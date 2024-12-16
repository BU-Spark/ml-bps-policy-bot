import os
import chainlit as cl
from rag_processor import RAGProcessor  # Import the RAG Processor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Set OpenAI API Key (Consider using environment variables in production)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize RAG Processor
rag_processor = RAGProcessor()

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
        # Process the query using the RAG processor
        full_response = rag_processor.process_query(message.content)

        # Send the response back to the user
        await cl.Message(content=full_response).send()

    except Exception as e:
        # Send the error message back to the user
        await cl.Message(content=f"An error occurred: {str(e)}").send()

if __name__ == "__main__":
    # This allows running the script directly if needed
    cl.run()
