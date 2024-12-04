"""
Main File for Boston Public School Policy Advisor Tool

This script uses LangChain, HuggingFace Transformers, FAISS, and OpenAI GPT models to create a 
retrieval-augmented generation (RAG) system. It retrieves policy documents related to Boston Public Schools 
and generates concise answers to user queries.

Key Components:
- HuggingFaceEmbeddings: To create vector representations of text.
- FAISS: For efficient similarity search in policy documents.
- OpenAI GPT (gpt-4o-mini): For answering user queries based on retrieved policies.

Author: Abhaya Shukla
Date: 12-04-2024
"""


from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI


load_dotenv()

print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))


# Define the path to the pre-trained model you want to use
modelPath = "sentence-transformers/all-MiniLM-l6-v2"

# Create a dictionary with model configuration options, specifying to use the CPU for computations
model_kwargs = {'device':'cpu'}

# Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
encode_kwargs = {'normalize_embeddings': False}

# Initialize an instance of HuggingFaceEmbeddings with the specified parameters
embeddings = HuggingFaceEmbeddings(
    model_name=modelPath,     # Provide the pre-trained model's path
    model_kwargs=model_kwargs, # Pass the model configuration options
    encode_kwargs=encode_kwargs # Pass the encoding options
)

loaded_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

retriever = loaded_db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0.1
    )

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import PromptTemplate
template = """You are the policy advisor for Boston Public School.Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that the question asked is beyond the scope of the policies.
Use three sentences maximum and keep the answer as concise as possible.
Also return the name of the policies referred to(given in the context)
{context}

Question: {question}

Answer: """

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
custom_rag_prompt = PromptTemplate.from_template(template)

rag_chain = (
    {
        "context": retriever | format_docs, "question": RunnablePassthrough()
    }
    |custom_rag_prompt
    |llm
    |StrOutputParser()
)


rag_chain.invoke("How does the District handle confidential health services for adolescent students?")
