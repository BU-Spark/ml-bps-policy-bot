import os
import re
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Path to the main dataset directory
dataset_path = './data/documents/dataset'
new_dataset_path = './data/documents/new_dataset'

# Initialize list to store all chunks and policies hashmap
all_chunks = []
policies = {}
folder_count = 0
pdf_count = 0

# Function to clean folder and file names
def clean_name(name):
    name = re.sub(r'\s*', '', name)
    name = re.sub(r'\.pdf$', '', name, flags=re.IGNORECASE)
    return name.strip()

# Function to get source link based on file name
def get_source_link(file_name):
    with open("./data/source_links.json", 'r') as file:
        url_mapping = json.load(file)
    for key in url_mapping:
        if key in file_name:
            return url_mapping[key]

BASE_URL = "https://www.bostonpublicschools.org/Page/5357"
def backup_source_link(folder_name):
    abbreviation = folder_name.split('(')[-1].replace(')', '')
    return f"{BASE_URL}#{abbreviation}"

# Function to process PDF
def process_pdf(pdf_path, folder_name):
    global pdf_count
    try:
        # Loading pdf
        loader = PyPDFLoader(file_path=pdf_path)
        docs_before_split = loader.load()

        if len(docs_before_split) == 0:
            print(f"Warning: No content found in {pdf_path}")
            return

        # Initialize the text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        # Split the documents into chunks
        docs_after_split = text_splitter.split_documents(docs_before_split)

        if len(docs_after_split) == 0:
            print(f"Warning: No chunks created from {pdf_path}")
            return

        # Clean folder and file names
        clean_folder_name = clean_name(folder_name)
        clean_file_name = clean_name(os.path.basename(pdf_path))

        # Add to policies hashmap
        abbreviation = folder_name.split('(')[-1].replace(')', '')
        if abbreviation not in policies:
            policies[abbreviation] = []
        policies[abbreviation].append(clean_file_name)

        # Prepare chunks with metadata
        for i, doc in enumerate(docs_after_split):
            chunk_data = {
                'folder_name': clean_folder_name,
                'file_name': clean_file_name,
                'chunk_id': i + 1,
                'content': doc.page_content,
                'source_link': get_source_link(clean_file_name),
                'backup_link': backup_source_link(clean_folder_name)
            }
            all_chunks.append(chunk_data)

        pdf_count += 1
        print(f"Processed {pdf_path}, created {len(docs_after_split)} chunks.")
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")

# Walk through the dataset directory and process all PDF files
for root, dirs, files in os.walk(dataset_path):
    if files:
        folder_count += 1
    for file_name in files:
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(root, file_name)
            folder_name = os.path.basename(root)
            process_pdf(pdf_path, folder_name)

# Save chunks to a JSON file
if all_chunks:
    output_path = './data/chunked_data_all_folders_with_links.json'
    with open(output_path, 'w') as json_file:
        json.dump(all_chunks, json_file, indent=4)
    print(f"All PDF chunks with links have been saved to {output_path}")
else:
    print("No chunks were created. Please check the input files.")

# Save policies hashmap to a JSON file
policies_output_path = './data/policies_hashmap.json'
with open(policies_output_path, 'w') as json_file:
    json.dump(policies, json_file, indent=4)
print(f"Policies hashmap has been saved to {policies_output_path}")

# Print statistics
print(f"Number of folders traversed: {folder_count}")
print(f"Number of PDFs processed: {pdf_count}")