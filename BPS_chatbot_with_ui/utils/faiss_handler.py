import faiss
import json
import numpy as np
from langchain.schema import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

def get_embeddings():
    # Initialize HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-l6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False}
    )
    return embeddings

# Load the JSON data
def json_to_documents(json_file_path = "./data/chunked_data_all_folders_with_links.json"):    
    with open(json_file_path, 'r') as json_file:
        chunked_data = json.load(json_file)

    # Initialize list to store documents
    documents = []

    # Process each entry in the JSON data
    for entry in chunked_data:
        # Extract fields from JSON entry
        original_content = entry['content']
        file_name = entry['file_name']
        source_link = entry.get('source_link', 'Unknown Source Link')
        backup_link = entry.get('backup_link', 'Unknown BackUp Link')

        # Create Document objects for each entry with metadata
        doc = Document(
            page_content=original_content,
            metadata={
                'file_name': file_name,
                'source_link': source_link,
                'backup_link': backup_link
            }
        )
        documents.append(doc)
    
    return documents

def save_faiss(db, index_path, metadata_path):
    # Save the FAISS index
    faiss.write_index(db.index, index_path)
    print(f"FAISS index saved to {index_path}")

    # Save metadata
    metadata_dict = {
        key: {
            "page_content": value.page_content,
            "metadata": value.metadata
        }
        for key, value in db.docstore._dict.items()
    }
    with open(metadata_path, 'w') as f:
        json.dump(metadata_dict, f, indent=4)
    print(f"Metadata saved to {metadata_path}")

def load_faiss_from_files(index_path, metadata_path, embedding_function):
    try:
        # Load FAISS index
        loaded_index = faiss.read_index(index_path)
        print(f"FAISS index loaded from {index_path}")

        # Load metadata
        with open(metadata_path, "r") as f:
            metadata_dict = json.load(f)
        print(f"Metadata loaded from {metadata_path}")

        # Ensure consistency between the index and metadata
        if loaded_index.ntotal != len(metadata_dict):
            raise ValueError(
                f"Mismatch between FAISS index vectors ({loaded_index.ntotal}) and metadata entries ({len(metadata_dict)})."
            )

        # Reconstruct the document store
        docstore = InMemoryDocstore({
            key: Document(page_content=value["page_content"], metadata=value["metadata"])
            for key, value in metadata_dict.items()
        })

        # Recreate the index_to_docstore_id mapping
        index_to_docstore_id = {i: key for i, key in enumerate(metadata_dict.keys())}

        # Recreate the FAISS database
        faiss_db = FAISS(
            index=loaded_index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id,
            embedding_function=embedding_function
        )
        print("FAISS database successfully reconstructed.")
        return faiss_db
    except Exception as e:
        print(f"Error loading FAISS data: {e}")
        return None

def ensure_index_idmap(faiss_index):
    # If the index is already an IndexIDMap, return it as-is
    if isinstance(faiss_index, faiss.IndexIDMap):
        return faiss_index

    # If the index is empty, wrap it in IndexIDMap
    if faiss_index.ntotal == 0:
        return faiss.IndexIDMap(faiss_index)

    # Recreate an empty IndexIDMap with the same structure
    dimension = faiss_index.d
    new_index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))

    # Transfer the existing data
    xb = faiss_index.reconstruct_n(0, faiss_index.ntotal)
    ids = np.arange(faiss_index.ntotal, dtype='int64')
    new_index.add_with_ids(xb, ids)

    print(f"Transferred {faiss_index.ntotal} vectors to a new IndexIDMap.")
    return new_index

def add_to_faiss(faiss_db, embeddings, documents):
    # Ensure the FAISS index is wrapped in IndexIDMap
    faiss_db.index = ensure_index_idmap(faiss_db.index)

    # Add documents to the FAISS index and docstore
    for i, doc in enumerate(documents):
        try:
            # Generate a unique vector ID for the document
            vector_id = hash(doc.metadata["file_name"] + str(i)) % (2**63 - 1)

            # Generate embedding for the document content
            vector = embeddings.embed_query(doc.page_content)

            # Add embedding to the FAISS index
            faiss_db.index.add_with_ids(
                np.array([vector]).astype("float32"),
                np.array([vector_id], dtype="int64")
            )

            # Add document metadata to the docstore
            faiss_db.docstore._dict[str(vector_id)] = doc

            # Update the index_to_docstore_id mapping
            faiss_db.index_to_docstore_id[vector_id] = str(vector_id)

        except Exception as e:
            print(f"Error adding document {doc.metadata.get('file_name', 'unknown')} to FAISS: {e}")

    print(f"Added {len(documents)} documents to the FAISS index.")
    return faiss_db

import numpy as np

def remove_from_faiss(faiss_db, file_name):
    # Identify all keys (IDs) associated with the file_name
    keys_to_remove = []
    for key, doc in list(faiss_db.docstore._dict.items()):
        if doc.metadata.get("file_name") == file_name:
            keys_to_remove.append(key)

    # If no matching content is found, return the FAISS database unmodified
    if not keys_to_remove:
        print(f"No content found in FAISS metadata for file_name: {file_name}")
        return faiss_db

    # Remove keys from the FAISS docstore and index
    numeric_ids = []
    for key in keys_to_remove:
        try:
            # Convert the key to an integer if possible
            numeric_id = int(key)
            numeric_ids.append(numeric_id)
        except ValueError:
            pass  # Skip non-numeric keys
        # Remove from docstore
        del faiss_db.docstore._dict[key]

    # Remove numeric IDs from the FAISS index
    if numeric_ids:
        # Convert numeric IDs to NumPy array
        numeric_ids = np.array(numeric_ids, dtype='int64')
        faiss_db.index.remove_ids(numeric_ids)

    print(f"Removed {len(keys_to_remove)} chunks related to file_name: {file_name}")

    # Debugging: Verify that no metadata for the file remains
    remaining_metadata = [
        doc.metadata for key, doc in faiss_db.docstore._dict.items()
        if doc.metadata.get("file_name") == file_name
    ]
    if remaining_metadata:
        print(f"WARNING: Metadata for file_name '{file_name}' still exists in docstore: {remaining_metadata}")
    else:
        print(f"Successfully removed all metadata for file_name: {file_name}")

    return faiss_db


def search_faiss(faiss_db, query, top_k=5):
    searchDocs = faiss_db.similarity_search(query, top_k=top_k)

    results = ""

    # Loop through relevant documents and format their content
    for i, doc in enumerate(searchDocs):
        results += f"Document {i+1} Content:\n{doc.page_content}\n{'-'*100}\n"

        file_name = doc.metadata.get("file_name", "None")
        results += f"File Name: {file_name}\n"

        source_link = doc.metadata.get("source_link", "None")
        results += f"Source Link: {source_link}\n"

        backup_link = doc.metadata.get("backup_link", "None")
        results += f"Backup Link: {backup_link}\n"

        results += f"{'='*100}\n\n"

    return results.strip()