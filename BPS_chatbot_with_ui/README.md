## **Setup and Installation**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Replace the "OPENAI_API_KEY" and "CHAINLIT_AUTH_SECRET" in .env
   You can generate CHAINLIT_AUTH_SECRET using: 
    ```bash
   chainlit create-secret
   ```

4. **Run the Application**:
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

1. **`source_links.json`**:
   - This file contains the all the links associated with each policy documnet
   - User should periodically update it to retrieve link from RAG model.  

2. **`vector_store/` Directory**:
   - Contains the FAISS index and metadata files for the embedded policy documents.
   - Files:
     - **`faiss_index`**: The FAISS index storing vector representations of document chunks for efficient similarity search.
     - **`faiss_meta.json`**: Metadata associated with the FAISS index, mapping vector IDs to the corresponding documents.

3. **`app.py`**:
   - Backend of the application
   - The main entry point of the application.
   - Implements the chatbot interface using Chainlit and OpenAI's GPT API.

4. **`utils/` Directory**:
   - Contains helper modules for core functionality:
     - **`faiss_handler.py`**: Handles FAISS embedding, index loading, saving, add to FAISS, remove from FAISS, and similarity searches.
     - **`chunker.py`**: Processes and splits policy documents into smaller chunks.

5. **`requirements.txt`**:
   - Lists all Python dependencies required for the project (e.g., Chainlit, FAISS, OpenAI API, etc.).

---

## **Usage**

1. **Admin and User**:
   - User can only retrieve policy documents
    - username: user
    - password: 123
   - Admin can retrieve policy documents, reindex the vector store, upload new document(s) to vector store, and remove specifc document from vector store.
    - username: admin
    - password: 321

2. **Reindex**:
   - Enter: 'reindex' on chatbot interface.
   - The application will re-chunk and re-embed the policy documents in `data/documents/dataset` directory.

3. **Upload**:
   - Attach the document(s) and source link(s) associated with each document(s) on chatbot interface
   - The application will chunk and embed ONLY the uploaded documents and add to vector store.

4. **Remove**:
   - Enter: 'remove: <file_name>' to remove specific document from vector store.
   - ex: remove: CAO-06 GPA Calculation Method
---

## **Error Management**

1. **Chainlit Timeout**:
   - When performing 'reindex', the chainlit will timeout during embedding process.
   - Admin can Stop Task after the console print: 
      - FAISS index saved to ./data/vector_store/faiss_index
      - Metadata saved to ./data/vector_store/faiss_meta

2. **Re-run reindex**:
   - When error occured, admin can run 'reindex' to fix the error.

3. **Contact**:
   - Contact: tedduoduo@gmail.com for any further issue.
