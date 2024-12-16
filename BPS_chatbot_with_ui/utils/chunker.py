import os
import re
import json
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clean_name(name):
    name = re.sub(r'\s*', '', name)
    name = re.sub(r'\.pdf$', '', name, flags=re.IGNORECASE)
    return name.strip()

def extract_abbreviation(folder_name):
    match = re.search(r'\((.*?)\)', folder_name)
    return match.group(1) if match else folder_name.split('-')[0]

def get_source_link(file_name):
    with open("./data/source_links.json", 'r') as file:
        url_mapping = json.load(file)
    file_name = clean_name(file_name)
    for key in url_mapping:
        if key in file_name:
            return url_mapping[key]
    return None

def add_to_source_link(file_name, source_link):
    source_links_path = "./data/source_links.json"
    
    # Ensure the source_links.json file exists
    if not os.path.exists(source_links_path):
        with open(source_links_path, 'w') as file:
            json.dump({}, file)  # Create an empty JSON object

    # Load the existing URL mappings
    with open(source_links_path, 'r') as file:
        url_mapping = json.load(file)

    # Clean the file name
    file_name = clean_name(file_name)

    # Add or update the mapping
    url_mapping[file_name] = source_link

    # Save the updated mappings back to the file
    with open(source_links_path, 'w') as file:
        json.dump(url_mapping, file, indent=4)

def backup_source_link(file_name):
    BASE_URL = "https://www.bostonpublicschools.org/Page/5357"
    abbreviation = file_name.split('-')[0]
    return f"{BASE_URL}#{abbreviation}"

def process_pdf(pdf_path, text_splitter):
    chunks = []
    try:
        loader = PyPDFLoader(file_path=pdf_path)
        docs_before_split = loader.load()
        if not docs_before_split:
            print(f"Warning: No content found in {pdf_path}. Skipping.")
            return chunks

        docs_after_split = text_splitter.split_documents(docs_before_split)
        if not docs_after_split:
            print(f"Warning: No chunks created from {pdf_path}. Skipping.")
            return chunks

        clean_file_name = clean_name(os.path.basename(pdf_path))

        for doc in docs_after_split:
            chunk_data = {
                'file_name': os.path.basename(pdf_path),
                'content': doc.page_content,
                'source_link': get_source_link(clean_file_name) or backup_source_link(clean_file_name),
                'backup_link': backup_source_link(clean_file_name),
            }
            chunks.append(chunk_data)

        print(f"Processed {pdf_path}, created {len(docs_after_split)} chunks.")
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return chunks

def process_dataset(dataset_path, output_chunk_path):
    all_chunks = []
    policies = {}
    folder_count = 0
    pdf_count = 0
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for root, _, files in tqdm(os.walk(dataset_path), desc="Processing folders"):
        if files:
            folder_count += 1
        for file_name in tqdm(files, desc="Processing PDFs", leave=False):
            if file_name.endswith('.pdf'):
                pdf_path = os.path.join(root, file_name)
                folder_name = os.path.basename(root)
                chunks = process_pdf(pdf_path, text_splitter)
                all_chunks.extend(chunks)

                abbreviation = extract_abbreviation(folder_name)
                clean_file_name = clean_name(file_name)
                if abbreviation not in policies:
                    policies[abbreviation] = []
                policies[abbreviation].append(clean_file_name)

                pdf_count += 1

    if all_chunks:
        with open(output_chunk_path, 'w') as json_file:
            json.dump(all_chunks, json_file, indent=4)
        print(f"All PDF chunks with links saved to {output_chunk_path}.")
    else:
        print("No chunks created. Please check the input files.")

    print(f"Number of folders traversed: {folder_count}")
    print(f"Number of PDFs processed: {pdf_count}")

if __name__ == "__main__":
    dataset_path = './data/documents/dataset'
    output_chunk_path = './data/chunked_data_all_folders_with_links.json'

    process_dataset(dataset_path, output_chunk_path)
