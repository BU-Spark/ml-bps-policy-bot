import openai
import os
import chainlit as cl
from openai import AsyncOpenAI
from utils.faiss_handler import *

# Initialize OpenAI client
client = AsyncOpenAI()

# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY")
cl.instrument_openai()

# OpenAI settings
settings = {
    "model": "gpt-4o",
    "temperature": 0.8,
}

index_path = "./data/vector_store/faiss_index"
meta_path = "./data/vector_store/faiss_meta"
embeddings = get_embeddings()
faiss_db = load_faiss_from_files(index_path, meta_path, embeddings)

@cl.on_message
async def on_message(message: cl.Message):
    global faiss_db
    if not faiss_db:
        await cl.Message(content="RAG model is not initialized. Please check the server setup.").send()
        return

    try:
        # Perform FAISS similarity search
        search_results = search_faiss(faiss_db, message.content)
        if not search_results:
            await cl.Message(content="No relevant documents found.").send()
            return
        
        await cl.Message(content=f"Processing...",).send()
        # Prepare messages for ChatGPT
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a generator of a RAG model for Boston Public School policies; "
                    "I will give you some retrieved documents from the RAG model; "
                    "reformat the content by summarizing it with bullet points," 
                    "remember to include links."
                    "Here is a sample with 3 important sections; Document #, Short Summary, and Source Links:"
                    "Document 1: policy file name here (XXX-02)"
                    "Source Links: Google Drive Document(s) | Official Website Link"
                    "Summary: one sentence summary. It covers:"
                    "bullet point 1"
                    "bullet point 2"
                    "bullet point 3"
                ),
            },
            {
                "role": "user",
                "content": search_results,
            },
        ]

        # Generate a summary using OpenAI
        response = await client.chat.completions.create(
            messages=messages,
            **settings
        )
        summary = response.choices[0].message.content

        # Send the summary back to the user
        await cl.Message(content=summary).send()

    except Exception as e:
        await cl.Message(content=f"Error generating summary: {e}").send()


