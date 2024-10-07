  
**Research phase**

*Paper 1: LLaMa-SciQ: An Educational Chatbot for Answering Science MCQ*  
[*https://arxiv.org/pdf/2409.16779*](https://arxiv.org/pdf/2409.16779)

* **Fine-Tuning for Accuracy**: Just as the LLaMa-SciQ project fine-tuned its language model for specific STEM topics, we can fine-tune our chatbot's natural language processing (NLP) model to better understand education-related queries. By training the model with actual policy documents, it will become more accurate at interpreting user questions and matching them to the right policies. This means teachers and staff will get more relevant results when they ask the chatbot questions like, "What’s the policy on student safety?"  
* **Optimizing Responses Based on User Preferences**: The **Direct Preference Optimization (DPO)** technique highlighted in the paper aligns the model’s responses with what users expect. We can use a similar approach by training our chatbot to understand which types of responses users prefer based on past interactions. This will help it provide more helpful and context-aware answers, especially when multiple policies could apply to a single query.  
* **Enhanced Document Retrieval**: Although the paper shows that Retrieval-Augmented Generation (RAG) didn’t always work perfectly, we can still apply this idea. Our chatbot can pull relevant information from multiple policy documents when users ask complex questions. For example, if someone asks, "What’s the procedure for reporting an incident and following up?" the chatbot can retrieve information from different sections of the policies and summarize it in one response.  
* **Efficient Processing**: The research also shows how quantization helps make the model faster without losing much accuracy. We can apply this in our project to make sure the chatbot responds quickly, even on lower-end devices or with limited server resources. This will be especially important if we want the system to scale across multiple institutions or school districts.  
* **Step-by-Step Explanations**: Finally, the **Chain-of-Thought (CoT)** reasoning used in LLaMa-SciQ can improve how our chatbot handles more detailed questions. For example, if a user asks, "How do I report a student incident, and what steps follow?" the chatbot can provide a clear, step-by-step explanation based on the relevant policy documents, making sure nothing important is left out.

*Paper 2: Developing a Llama-Based Chatbot for CI/CD Question Answering: A Case Study at Ericsson*  
[*https://arxiv.org/pdf/2408.09277*](https://arxiv.org/pdf/2408.09277)

* **Domain-Specific corpus creation:** Just as the CI/CD chatbot uses a domain-specific corpus built from internal documents and conversations, we can build a similar corpus from school policy documents. By extracting and preprocessing documents —the chatbot will have a solid base for retrieving accurate information. This will ensure that when higher management or attorneys ask questions like "What are all the laws that are required reporting or filling  bullying incidents?" The chatbot will retrieve relevant sections from multiple documents and provide a precise answer.  
* **Data Preprocessing and Contextual Compression for Improved Accuracy**: We can follow a similar approach by preprocessing policy documents—removing unnecessary formatting, linking related sections, and organizing documents into smaller, manageable chunks. This will allow the chatbot to better focus on the specific sections of the policies relevant to the user’s query, here the method restates the user query in more precise terms to improve retrieval accuracy. By applying techniques like contextual compression, we can minimize irrelevant information, making sure users receive precise, policy-driven answers.  
* **Retrieval-Augmented Generation (RAG) for Enhanced Document Retrieval**: Similar to the RAG model used in the CI/CD chatbot, we can implement a retrieval-augmented approach to pull relevant policies for complex user queries. In situations where multiple policies or regulations may apply, such as when a user asks, "What are the steps for handling a student safety violation?" The chatbot will retrieve and consolidate information from different policy sections, ensuring a comprehensive response. Even though RAG has some limitations, it remains a powerful tool for generating accurate and contextually relevant answers in complex domains like school policies.  
* **Query Rewriting for Better User Experience**: The chatbot described in the paper uses query rewriting to clarify user queries, which improves retrieval accuracy. For our chatbot, this means rephrasing vague or unclear questions posed by school staff to ensure they retrieve the most relevant policies. For instance, if a user asks, "How do I handle a student misconduct report?" the chatbot could rewrite the query into a more specific form, like "What are the reporting steps for student misconduct as per district guidelines?" This will optimize the accuracy of the retrieved policies.  
* **Error Handling and Hallucination Prevention**: The error analysis in the paper highlights the challenges of language models hallucinating or providing inaccurate responses. For our policy chatbot, implementing safeguards to prevent hallucination is essential, particularly in a legal or educational context where inaccurate answers could have significant consequences. Ensuring that the chatbot strictly relies on retrieved policy documents rather than generating unsupported content will improve trust and accuracy.

*Paper 3: FACTS About Building Retrieval Augmented Generation-based Chatbots*  
[*https://arxiv.org/pdf/2407.07858*](https://arxiv.org/pdf/2407.07858)

* **Hybrid Search Implementation**: The paper highlights the advantages of combining lexical and vector-based search methods. By integrating this hybrid search into our chatbot, we think it can significantly improve the accuracy and relevance of retrieved school policy documents, ensuring users quickly find the information they need.  
* **Agentic Architectures for Complex Queries**: The paper emphasizes the need for agentic architectures capable of decomposing complex queries. This feature will be valuable for our chatbot when users pose multifaceted questions regarding policy documents, enabling it to provide precise and context-aware answers​.  
* **Fine-Tuning Techniques**: The paper presents several fine-tuning strategies for large language models (LLMs), such as prompt engineering and parameter-efficient training. Implementing these techniques will allow us to customize our chatbot's responses to better align with the specific needs and language used in school policy documents.  
  


*Paper 4: RQ-RAG: Learning to Refine Queries for Retrieval Augmented Generation*  
[*https://arxiv.org/pdf/2404.00610*](https://arxiv.org/pdf/2404.00610)  
**Query Refinement Mechanism:** RQ-RAG introduces a method for refining user queries before they are sent to the retrieval system. By incorporating a query refinement layer in our chatbot, we can ensure that ambiguous or complex user queries related to public policy documents are clarified and simplified. This refinement can lead to more effective retrieval of relevant documents, as the system will better understand the user's intent.

**Multi-Step Query Processing:** The multi-step processing framework described allows the model to iteratively improve the quality of queries before document retrieval. We can apply this technique to create a multi-turn interaction model, where the chatbot can ask clarifying questions to users, ensuring it retrieves the most relevant policy documents. For example, if a user inquires about procedures for a meeting, the chatbot can ask for specifics like the type of meeting (e.g., parent-teacher) before retrieving documents.

**Dual-Retriever Framework:** RQ-RAG uses two retrievers—one for coarse retrieval and one for refined, context-aware retrieval. The coarse retriever initially retrieves a set of broad documents based on the user's input. The system then passes these documents and the original query to a fine retriever, which uses additional context to refine the search and retrieve more relevant documents. This process involves training both retrievers: one to handle general searches and the other to handle refined context-sensitive queries. This approach can be integrated into our system to enhance the chatbot's ability to fetch more accurate documents by first retrieving a broader set of documents and then refining the query based on the initial results.

*Open-source project :*

1. RAG Chatbot:  
   [https://github.com/umbertogriffo/rag-chatbot](https://github.com/umbertogriffo/rag-chatbot)  
   The rag-chatbot repository offers several components that can significantly enhance our chatbot project for BPS:  
* **Retrieval-Augmented Generation (RAG):** This approach retrieves relevant document sections based on user queries and improves response accuracy. Using this in our project will enhance how the chatbot pulls policy documents.  
* **Memory Indexing:** We can enable faster, more accurate document retrieval by chunking documents and storing their embeddings in a vector database like **Chroma**.  
* **Context Handling:** Methods like **Hierarchical Summarization** and **Create and Refine** can help our chatbot handle large or complex queries across multiple documents.

The following research papers and one open-source project reference have been thoroughly read, and there is a clear explanation of how some of these methods and techniques are used in our chatbot implementation.

**Contributors:**

1. Akshat Gurbuxani  
2. Abhaya Shukla   
3. Akuraju Mounika Chowdary   
4. Duoduo Xu