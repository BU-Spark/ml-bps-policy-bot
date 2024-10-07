# Boston Public School Policy Document Retrieval Chatbot

Project Overview

This project aims to streamline access to policy documents within educational and public institutions. The chatbot system will help users quickly locate specific information from disorganized or complex file structures by reorganizing documents intelligently. This system will enhance accessibility, save time, and improve user experience.

 Key Features:

1. Simplified document navigation: The chatbot will make it easy for users to search for and retrieve relevant policy documents.  
2. AI/ML-powered: Machine learning models will be used to interpret user queries and rank policy documents by relevance.  
3. Document reorganization: The system will suggest improvements to document categorization based on user behavior and queries.

 B. Problem Statement

1\. Natural Language Understanding for Query Interpretation:

* Task: Develop an NLP model to interpret user queries and map them to policy categories.  
* Objective: Classify user input into predefined categories and extract key details.  
* Approach: Use text classification and named entity recognition (NER), leveraging fine-tuned large language models (LLMs).

2\. Document Retrieval and Ranking:

* Task: Build a document retrieval system that searches the repository and returns the most relevant documents.  
* Objective: Use techniques like vector embeddings to rank documents by relevance.  
* Approach: Implement semantic search with LLM-based embeddings or retrieval models like BM25 or dense retrieval.

C. Project Checklist

1\. Data Preparation and Preprocessing:

* Data scraping: Collect policy documents from the repository.  
* Data cleaning: Remove duplicates, incomplete, and irrelevant data.  
* Tokenization: Break text into tokens for processing.  
* Metadata Tagging: Assign metadata like policy numbers and names.

2\. Query Interpretation:

* Text Classification Model: Implement a model for interpreting and categorizing user queries.  
* Intent Recognition: Define logic to map user queries to relevant document categories.

3\. Document Retrieval System:

* Vector Embeddings: Develop a system to retrieve documents based on vector embeddings.  
* Semantic Search Engine: Implement a search engine to rank documents by relevance.

4\. Fine-tuning and Evaluation:

* Refine Models: Continuously improve model performance based on feedback and evaluation metrics (e.g., accuracy, precision, recall).

5\. User Interface and Chatbot Integration:

* Chatbot Deployment: Integrate the chatbot with a web interface for user interaction and document retrieval.

D. Operationalization Path

The chatbot will be deployed on a web interface where users can ask questions in natural language (e.g., "How do I report an incident?"). The system will retrieve the most relevant policy documents and provide direct answers, helping users navigate the policy repository efficiently.

Resources:

https://www.bostonpublicschools.org/domain/1884

Contributors:  
Akshat Gurbuxani  
Abhaya Shukla  
Akuraju Mounika Chowdary  
Duoduo Xu