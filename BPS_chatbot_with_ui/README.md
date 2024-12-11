## **Setup and Installation**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Requirements**:
   - Use the `Makefile` to install all necessary dependencies:
     ```bash
     make install-requirements
     ```
   - Alternatively, you can manually install requirements:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   - Start the chatbot interface:
     ```bash
     chainlit run app.py -w
     ```

---

## **Project Structure**

### **Key Files and Directories**

1. **`chunked_data_all_folders_with_links.json`**:
   - This file contains the chunked policy documents with metadata such as folder name, file name, source link, and backup link.
   - Each entry in the file represents a document chunk with the following structure:
     ```json
     {
       "content": "Document chunk content here...",
       "folder_name": "Policy Folder Name",
       "file_name": "Policy Document Name",
       "source_link": "Original document source link",
       "backup_link": "Backup document link"
     }
     ```

2. **`vector_store/` Directory**:
   - Contains the FAISS index and metadata files for the embedded policy documents.
   - Files:
     - **`faiss_index`**: The FAISS index storing vector representations of document chunks for efficient similarity search.
     - **`faiss_meta.json`**: Metadata associated with the FAISS index, mapping vector IDs to the corresponding documents.

3. **`app.py`**:
   - The main entry point of the application.
   - Implements the chatbot interface using Chainlit and OpenAI's GPT API.
   - Handles loading the FAISS index, performing similarity searches, and generating summaries.

4. **`Makefile`**:
   - Simplifies project setup and execution.
   - Commands:
     - **`make install-requirements`**: Installs all Python dependencies from `requirements.txt`.

5. **`utils/` Directory**:
   - Contains helper modules for core functionality:
     - **`faiss_handler.py`**: Handles FAISS embedding, index loading, saving, and similarity searches.
     - **`pdf_processor.py`**: Processes and splits policy documents into smaller chunks.

6. **`requirements.txt`**:
   - Lists all Python dependencies required for the project (e.g., Chainlit, FAISS, OpenAI API, etc.).

---

## **Environment Variables**

Ensure the following environment variables are set for the application to function correctly:

- **`OPENAI_API_KEY`**: Your OpenAI API key for accessing GPT models.
- **`CHAINLIT_HOST`**: (Optional) The host for the Chainlit interface (default: `localhost`).
- **`CHAINLIT_PORT`**: (Optional) The port for the Chainlit interface (default: `8000`).

---

## **Workflow**

1. **Chunking Policy Documents**:
   - Policy documents are preprocessed and split into smaller, manageable chunks using `pdf_processor.py`.
   - Chunk metadata is stored in `chunked_data_all_folders_with_links.json`.

2. **Embedding and FAISS Index**:
   - Document chunks are embedded into vector representations using a pre-trained embedding model (e.g., `sentence-transformers/all-MiniLM-l6-v2`).
   - The FAISS index and associated metadata are stored in the `vector_store/` directory.

3. **Chatbot Interaction**:
   - The chatbot queries the FAISS index to retrieve relevant document chunks for user queries.
   - Retrieved chunks are passed to OpenAI's GPT model for summarization.
   - The summarized response is displayed to the user.

---