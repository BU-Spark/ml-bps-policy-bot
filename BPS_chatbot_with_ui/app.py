import openai
import os
import tempfile
import asyncio
import re
import chainlit as cl
from openai import AsyncOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.faiss_handler import *
from utils.chunker import *

# Initialize OpenAI client
client = AsyncOpenAI()

# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY")
cl.instrument_openai()

# OpenAI settings
settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.5,
}

dataset_path = "./data/documents/dataset"
output_chunk_path = "./data/chunked_data_all_folders_with_links.json"
index_path = "./data/vector_store/faiss_index"
meta_path = "./data/vector_store/faiss_meta"
embeddings = get_embeddings()
faiss_db = load_faiss_from_files(index_path, meta_path, embeddings)

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "321"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    elif (username, password) == ("user", "123"):
        return cl.User(
            identifier="user", metadata={"role": "user", "provider": "credentials"}
        )
    else:
        return None

@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get("user")
    if user:
        if user.identifier == "admin":
            await cl.Message(content="Welcome Admin! You can:\n"
                            "- Send a policy-related question.\n"
                            "- Upload new documents (attach with source links).\n"
                            "- Enter: 'reindex' to re-chunk and re-embed the FAISS vector store.\n"
                            "- Enter: 'remove: <file name>' to remove a document.").send()
        else:
            await cl.Message(content="Hi! I will assist you in finding documents based on your question. Let's get started!").send()

@cl.on_message
async def handle_user_message(message: cl.Message):
    user = cl.user_session.get("user")
    try:
        if user and user.identifier == "admin":
            if message.content.lower() == "reindex":
                await reindex()
            elif message.content.lower().startswith("remove:"):
                await remove_doc(message)
            elif message.elements:
                await process_uploaded_files(message)
            else:
                await perform_chatgpt_query(message)
        else:
            await perform_chatgpt_query(message)
    except Exception as e:
        await cl.Message(content=f"Error handling your request: {e}").send()

async def process_uploaded_files(message):
    global faiss_db
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Extract source links from the user's message
    url_pattern = r'https?://[^\s]+'
    source_links = re.findall(url_pattern, message.content)

    files = [file for file in message.elements if "pdf" in file.mime]
    if len(files) != len(source_links):
        await cl.Message(content=f"Error: Number of links ({len(source_links)}) and uploaded files ({len(files)}) do not match.").send()
        return

    all_chunks = []
    try:
        for file, source_link in zip(files, source_links):
            if not file.path or not os.path.exists(file.path):
                raise ValueError(f"Invalid file path for {file.name}.")

            with open(file.path, "rb") as f:
                file_content = f.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name

            # Remove document before update
            faiss_db = remove_from_faiss(faiss_db, file.name)

            loader = PyPDFLoader(temp_path)
            document = loader.load()
            chunks = text_splitter.split_documents(document)

            for chunk in chunks:
                chunk.metadata = chunk.metadata or {}
                chunk.metadata.update({
                    "file_name": file.name,
                    "source_link": source_link,
                    "backup_link": backup_source_link(clean_name(file.name)),
                })
                # Remove 'page' and 'source'
                chunk.metadata.pop("page", None)
                chunk.metadata.pop("source", None)

            all_chunks.extend(chunks)
            os.remove(temp_path)

        # Update FAISS database
        faiss_db = add_to_faiss(faiss_db, embeddings, all_chunks)
        save_faiss(faiss_db, index_path, meta_path)
        await cl.Message(content=f"Added {len(all_chunks)} chunks to FAISS vector store.").send()

    except Exception as e:
        await cl.Message(content=f"Error during file processing: {e}").send()

async def perform_chatgpt_query(message: cl.Message):
    if not faiss_db:
        await cl.Message(content="FAISS vector store is not initialized.").send()
        return

    try:
        search_results = search_faiss(faiss_db, message.content)
        if not search_results:
            await cl.Message(content="No relevant documents found.").send()
            return

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant for Boston Public School policies. I will provide you with retrieved documents from the RAG model. Your task is to:"
                    "1. Refuse to engage with harmful, racist, or discriminatory questions. If such a query is detected, respond only with: I'm sorry, but I cannot assist with that request."
                    "2. Evaluate the relevance of each document based on its content and the query provided."
                    "3. Only summarize documents that are relevant to the query. A document is considered relevant if it contains policies or guidelines explicitly related to the query."
                    "4. If a document is not at least somewhat relevant, exclude it from the summary."
                    "5. Do not return anything other than reformatted or summarized documents"
                    "6. Remember to include the link"
                    "For relevant documents, reformat the content in this structured format:"
                    "Document: Policy file name here\n"
                    "Formatting Links: Google Drive Link (format Google Drive Link here)| Boston Public School Link (format Boston Public School Link here)\n"
                    "Summary: write 2-3 sentences summary.\n"
                    "Key points (1 sentence)"
                    "- [Bullet point 1]\n"
                    "- [Bullet point 2]\n"
                    "- [Bullet point 3]\n" 
                    "NO ADDITIONAL TEXT AFTER THIS!"
                    ),
            },
            {"role": "user", "content": search_results},
        ]

        response = await client.chat.completions.create(messages=messages, **settings)
        await cl.Message(content=response.choices[0].message.content).send()

    except Exception as e:
        await cl.Message(content=f"Error generating response: {e}").send()

async def reindex():
    global faiss_db
    try:
        await cl.Message(content="Reindexing in progress...").send()
        process_dataset(dataset_path=dataset_path, output_chunk_path=output_chunk_path)

        await cl.Message(content="chunks created successfully. Now embedding...").send()
        documents = json_to_documents(output_chunk_path)
        faiss_db = FAISS.from_documents(documents, embeddings)
        save_faiss(faiss_db, index_path, meta_path)
    except Exception as e:
        await cl.Message(content=f"Error during reindexing: {e}").send()

async def remove_doc(message):
    global faiss_db

    try:
        file_name = message.content.split("remove:", 1)[1].strip()
        file_name = file_name + ".pdf"
        faiss_db = remove_from_faiss(faiss_db, file_name)
        save_faiss(faiss_db, index_path, meta_path)
        await cl.Message(content=f"Document '{file_name}' removed from FAISS vector store.").send()
    except Exception as e:
        await cl.Message(content=f"Error removing document: {e}").send()
