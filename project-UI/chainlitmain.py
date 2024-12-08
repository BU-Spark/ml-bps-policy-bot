import chainlit as cl
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os
import json

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"  

# Initialize Embeddings and FAISS
modelPath = "sentence-transformers/all-MiniLM-l6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=modelPath,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

# Load FAISS Index
loaded_db = FAISS.load_local("code/faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = loaded_db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# LLM Configuration
llm = ChatOpenAI(model="gpt-4o-mini")

# Prompt Template
template = """
You are a highly knowledgeable and professional policy advisor for Boston Public Schools. Your role is to provide precise, context-specific answers to questions based solely on the information provided in the context. 

### Guidelines:
1. **Scope Limitation**: Only use the information provided in the "Context" to answer the question. Do not infer, assume, or incorporate external information.
2. **Out-of-Scope Questions**: If a question is unrelated to any policy, politely respond that it is beyond the scope of your knowledge as a policy advisor and feel free to continue the answer based on the "question". Finally, append "[0]__[0]" at the end of the answer for the developer to use, only if the "question" is unrelated to the task. 
3. **Citing Policy**: Always conclude your response by explicitly citing the policy name(s) used to formulate your answer. If no policy is applicable, don't mention anything.

### Additional Considerations:
- **Ambiguities**: If the context lacks sufficient information to answer the question definitively, mention this and provide a response based on the provided context.
- **Clarity and Professionalism**: Ensure all responses are concise but comprehensive, clear, and professional.

### Input Structure:
Context: {context}
Question: {question}
"""

custom_rag_prompt = PromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(
        f"{doc.page_content}\n\nSource: {doc.metadata.get('file_name', 'Unknown File')}, Folder: {doc.metadata.get('folder_name', 'Unknown Folder')}"
        for doc in docs
    )

rag_chain = (
    {
        "context": retriever | format_docs, 
        "question": RunnablePassthrough()
    }
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

@cl.on_chat_start
async def on_chat_start():
    """
    Initializes the chatbot session.
    """
    await cl.Message(
        content="Hi! I am the policy advisor for Boston Public School. How can I assist you today?"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handles user queries and returns answers based on retrieved documents.
    """
    try:
        # Invoke the RAG chain to get the main response
        response = rag_chain.invoke(message.content)

        marker = "[0]__[0]"
        # Check if the response contains the marker
        if marker in response:
            # Remove the marker from the response
            full_response = response.replace(marker, "").strip()
        else:
            # Retrieve relevant documents
            retrieved_documents = retriever.invoke(message.content)
            
            # Initialize a list to collect formatted links
            links = []
            for i, item in enumerate(retrieved_documents, 1):  # Iterate through the list of Document objects
                link = item.metadata.get('link')  # Access the 'link' key within the 'metadata' attribute
                file_name = item.metadata.get('file_name')  # Access the 'file_name' key within the 'metadata' attribute
                if link:
                    # Append each link in Markdown format for clickability
                    links.append(f"**Source {i}:** [{file_name}]({link})")

            # Join the response with links, separating links by a new line
            full_response = f"{response}\n\n**References:**\n" + "\n".join(links) if links else response

        # Send the response back to the user
        await cl.Message(content=full_response).send()

    except Exception as e:
        # Send the error message back to the user
        await cl.Message(content=f"An error occurred: {str(e)}").send()
