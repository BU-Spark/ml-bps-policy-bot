# Technical Project Document

## *Akshat Gurbuxani, Abhaya Shukla, Akuraju Mounika Chowdary, Duoduo Xu,  2024-Sep-29 v1.0.0-dev*

## Project Overview

In educational and public institutions, locating the right policy documents can be difficult due to disorganized and complex file structures. This project aims to streamline access to these documents by developing a chatbot system that smartly reorganizes them and helps users quickly find specific information. By simplifying navigation through the policy database, the system will enhance document accessibility, save time, and improve the overall user experience.

### **A. Human to AI Process**

**Time-Consuming Searches**: Users often waste time sifting through irrelevant documents.  
**Inefficient Document Management**: Organizing files becomes increasingly difficult as the volume of documents grows.  
**Dependence on Human Assistance**: Users frequently need help from administrators or colleagues to navigate the repository.  
**Manual Data Analysis for Reorganization**: Tracking user behavior and identifying reorganization needs is extremely slow and inefficient, as it depends on manual reporting.  
**Inconsistent Naming & Categorization**: Non-intuitive naming and categorization make it difficult for users to locate necessary documents.

The goal of implementing AI/ML is to automate and streamline the above processes, improving the efficiency of document management, query resolution, and user experience through a chatbot interface. Machine learning models can be trained to understand user queries, locate relevant documents quickly, and even suggest organizational improvements to the document repository, minimizing human effort and speeding up the process.

**B. Problem Statement**

1. *Natural Language Understanding for Query Interpretation*  
   **Task**: Develop an NLP model that accurately interprets user queries, mapping them to relevant policy categories such as Superintendent's Circulars or Policies & Procedures.  
   **Objective**: Classify user input into predefined categories and extract key details necessary to retrieve the correct document.  
   **Approach**: Implement text classification and named entity recognition (NER) models, potentially leveraging fine-tuned large language models (LLMs) to improve query interpretation and understanding.  
2. *Document Retrieval and Ranking*  
   **Task**: Create a robust document retrieval system that searches the policy repository and returns the most relevant documents based on the interpreted user query.  
   **Objective**: Employ techniques like vector embeddings (e.g., TF-IDF, BERT) to rank documents by relevance, ensuring the user receives the most appropriate policy document.  
   **Approach**: Utilize semantic search with LLM-based embeddings or specialized retrieval models such as BM25 or dense retrieval models for optimal ranking.

### **C. Project Checklist**

1. *Data Preparation and Preprocessing*   
   1. Data scraping: Collect policy documents and relevant data from the repository.  
   2. Data cleaning: Remove duplicates, incomplete data, and irrelevant content.  
   3. Tokenization: Break down text into manageable tokens for processing.  
   4. Metadata Tagging: Assigning descriptive metadata to documents, such as policy numbers and names.  
2. *Query Interpretation*  
   1. Text Classification Model: Implement a model to interpret user queries and classify them into predefined categories.  
   2. Intent Recognition: Define logic for recognizing user intents and mapping queries to relevant document categories.  
3. *Document Retrieval System*   
   1. Vector Embeddings: Develop a document retrieval system using vector embeddings  
   2. Semantic Search Engine: Implement a semantic search engine to retrieve the most relevant policy documents  
4. *Fine-tuning and Evaluating the Model*

    Refine models based on user feedback and performance metrics (e.g., accuracy, precision, recall).

5. *User Interface and Chatbot Integration*

   Chatbot Deployment: Integrate the chatbot into the website to allow users to interact and retrieve documents to understand applicable policies.

### **D. Operationalization Path**

**Web-Based Chatbot for Policy Assistance**: Teachers and staff will interact with the chatbot through a user-friendly web interface, where they can ask policy-related questions in natural language (e.g., "How do I report an incident?"). The chatbot will respond by retrieving the most relevant policy documents and offering direct answers based on a comprehensive policy repository. This system will simplify access to crucial information, making it faster and easier for users to find what they need.

## Resources

### Data Sets

* The dataset is accessible on the website linked below

	Link: https://www.bostonpublicschools.org/domain/1884

### References

1. BPS dataset. [Policies and Procedures: Superintendent's Circulars](https://www.bostonpublicschools.org/domain/1884)

## Weekly Meeting Updates

Link to Minutes of Meeting(MoM): [MoM](https://docs.google.com/document/d/1wGxGDV2dEWZpbn51u630e4QiFFTHfj-zjwMHe8bGOHs/edit?usp=sharing)

| Week | What is done? | What is next? |
| :---- | :---- | :---- |
| 1 | Team Agreement | Project Outline |
| 2 | Project Outline | Data Scraping  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |
| 9 |  |  |

