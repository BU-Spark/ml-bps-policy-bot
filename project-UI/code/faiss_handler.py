import faiss
import numpy as np

# Helper Functions
def ensure_index_idmap(faiss_index):
    if isinstance(faiss_index, faiss.IndexIDMap):
        return faiss_index
    if faiss_index.ntotal == 0:
        return faiss.IndexIDMap(faiss_index)
    dimension = faiss_index.d
    new_index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))
    xb = faiss_index.reconstruct_n(0, faiss_index.ntotal)
    ids = np.arange(faiss_index.ntotal, dtype='int64')
    new_index.add_with_ids(xb, ids)
    return new_index

def faiss_add(faiss_db, embeddings, documents):
    faiss_db.index = ensure_index_idmap(faiss_db.index)
    for i, doc in enumerate(documents):
        try:
            vector_id = hash(doc.metadata["file_name"] + str(i)) % (2**63 - 1)
            vector = embeddings.embed_query(doc.page_content)
            faiss_db.index.add_with_ids(
                np.array([vector]).astype("float32"),
                np.array([vector_id], dtype="int64")
            )
            faiss_db.docstore._dict[str(vector_id)] = doc
            faiss_db.index_to_docstore_id[vector_id] = str(vector_id)
        except Exception as e:
            print(f"Error adding document {doc.metadata.get('file_name', 'unknown')} to FAISS: {e}")
    return faiss_db

def faiss_remove(faiss_db, file_name):
    keys_to_remove = [
        key for key, doc in faiss_db.docstore._dict.items()
        if doc.metadata.get("file_name") == file_name
    ]
    numeric_ids = [int(key) for key in keys_to_remove if key.isdigit()]
    if numeric_ids:
        faiss_db.index.remove_ids(np.array(numeric_ids, dtype="int64"))
    for key in keys_to_remove:
        del faiss_db.docstore._dict[key]
    return faiss_db
