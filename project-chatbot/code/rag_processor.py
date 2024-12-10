import os
from typing import List, Optional

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

class RAGProcessor:
    def __init__(
        self, 
        embedding_model: str = "sentence-transformers/all-MiniLM-l6-v2",
        faiss_index_path: str = "code/faiss_index",
        llm_model: str = "gpt-4o-mini"
    ):
        """
        Initialize RAG Processor with configurable parameters.
        
        Args:
            embedding_model (str): Path to embedding model
            faiss_index_path (str): Path to FAISS index
            llm_model (str): Language model to use
        """
        # Initialize Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        
        # Load FAISS Index
        self.vector_store = FAISS.load_local(
            faiss_index_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        
        # Configure Retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 4}
        )
        
        # Configure LLM
        self.llm = ChatOpenAI(model=llm_model)

    def _format_documents(self, docs: List[Document]) -> str:
        """
        Format retrieved documents into a readable string.
        
        Args:
            docs (List[Document]): Retrieved documents
        
        Returns:
            str: Formatted document string
        """
        return "\n\n".join(
            f"{doc.page_content}\n\nSource: {doc.metadata.get('file_name', 'Unknown File')}, Folder: {doc.metadata.get('folder_name', 'Unknown Folder')}"
            for doc in docs
        )

    def create_rag_prompt(self, custom_template: Optional[str] = None) -> PromptTemplate:
        """
        Create a RAG prompt template.
        
        Args:
            custom_template (Optional[str]): Custom prompt template
        
        Returns:
            PromptTemplate: Configured prompt template
        """
        default_template = """
        You are a highly knowledgeable and professional policy advisor for Boston Public Schools. Your role is to provide precise, context-specific answers to questions based solely on the information provided in the context. 

        ### Guidelines:
        1. **Scope Limitation**: Only use the information provided in the "Context" to answer the question. Do not infer, assume, or incorporate external information.
        2. **Out-of-Scope Questions**: If a question is unrelated to any policy, politely respond that it is beyond the scope of your knowledge as a policy advisor and feel free to continue the answer based on the "question". Do not mention anything that you're unsure of. If you're unsure of the question or its relation to the context, acknowledge this in your response. Finally, append "[0]__[0]" at the end of the answer for the developer to use, only if the "question" is unrelated to the task. 
        3. **Citing Policy**: Always conclude your response by explicitly citing the policy name(s) used to formulate your answer. If no policy is applicable, don't mention anything.

        ### Additional Considerations:
        - **Ambiguities**: If the context lacks sufficient information to answer the question definitively, mention this and provide a response based on the provided context.
        - **Clarity and Professionalism**: Ensure all responses are concise but comprehensive, clear, and professional.

        ### Input Structure:
        Context: {context}
        Question: {question}
        """
        
        template = custom_template or default_template
        return PromptTemplate.from_template(template)

    def create_rag_chain(self, custom_template: Optional[str] = None):
        """
        Create a RAG (Retrieval-Augmented Generation) chain.
        
        Args:
            custom_template (Optional[str]): Custom prompt template
        
        Returns:
            Configured RAG chain
        """
        prompt = self.create_rag_prompt(custom_template)
        
        rag_chain = (
            {
                "context": self.retriever | self._format_documents, 
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain

    def get_references(self, query: str) -> List[str]:
        """
        Retrieve reference links for a given query.
        
        Args:
            query (str): User query
        
        Returns:
            List[str]: Formatted reference links
        """
        retrieved_documents = self.retriever.invoke(query)
        
        links = []
        seen_links = set()

        for item in retrieved_documents:
            link = item.metadata.get('link')
            file_name = item.metadata.get('file_name')
            if link and link not in seen_links: 
                seen_links.add(link) 
                links.append(f"**Source {len(links) + 1}:** [{file_name}]({link})")

        return links

    def process_query(self, query: str, custom_template: Optional[str] = None) -> str:
        """
        Process a user query and return the response with optional references.
        
        Args:
            query (str): User query
            custom_template (Optional[str]): Custom prompt template
        
        Returns:
            str: Processed response with optional references
        """
        rag_chain = self.create_rag_chain(custom_template)
        response = rag_chain.invoke(query)

        marker = "[0]__[0]"
        if marker in response:
            full_response = response.replace(marker, "").strip()
        else:
            links = self.get_references(query)
            full_response = f"{response}\n\n**References:**\n" + "\n".join(links) if links else response

        return full_response
