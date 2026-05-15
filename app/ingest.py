import os
import sys
import shutil
import argparse
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils import get_file_hash, load_processed_files, save_processed_files, log_audit
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
CHROMA_DIR = "data/metadata/chroma_db"
INCOMING_DIR = "data/incoming"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def copy_to_incoming(source_path, category="incoming"):
    """Copy a file into the incoming folder, preserving original extension."""
    os.makedirs(INCOMING_DIR, exist_ok=True)
    dest = os.path.join(INCOMING_DIR, category, os.path.basename(source_path))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(source_path, dest)
    return dest

def ingest_files(file_paths, category="incoming"):
    """Ingest a list of file paths (absolute or relative)."""
    processed = load_processed_files()
    new_files = []
    for fp in file_paths:
        if not os.path.exists(fp):
            print(f"?? File not found: {fp}")
            continue
        # Compute hash of original file
        file_hash = get_file_hash(fp)
        if file_hash not in processed:
            # Copy to incoming folder
            local_copy = copy_to_incoming(fp, category)
            new_files.append((fp, local_copy))
        else:
            print(f"? Already ingested: {fp}")
    if not new_files:
        print("No new files to ingest.")
        return

    print(f"?? Ingesting {len(new_files)} new file(s)...")
    docs = []
    for original, copy_path in new_files:
        if copy_path.endswith('.pdf'):
            loader = PyPDFLoader(copy_path)
        elif copy_path.endswith('.docx'):
            loader = UnstructuredWordDocumentLoader(copy_path)
        else:
            loader = TextLoader(copy_path)
        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    for chunk in chunks:
        chunk.metadata["category"] = category
        chunk.metadata["source_file"] = original  # keep original path

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    vectorstore.add_documents(chunks)
    # Chroma auto-persists after each add

    # Mark as processed using original file hash
    for original, _ in new_files:
        processed[get_file_hash(original)] = original
    save_processed_files(processed)
    for original, _ in new_files:
        log_audit("INGEST", original, f"Chunks: {len(chunks)}")
    print(f"? Ingested {len(chunks)} chunks from {len(new_files)} file(s) as category '{category}'")

def ingest_folder(folder_path, category="incoming"):
    """Recursively find all supported files in a folder and ingest them."""
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith(('.pdf', '.txt', '.docx')):
                all_files.append(os.path.join(root, f))
    print(f"Found {len(all_files)} files in {folder_path}")
    ingest_files(all_files, category)

def ingest_default_folders():
    """Original behaviour: scan data/policies, data/architecture, data/product_docs."""
    default_cats = {
        "data/policies": "policy",
        "data/architecture": "architecture",
        "data/product_docs": "product"
    }
    for folder, cat in default_cats.items():
        if os.path.exists(folder):
            # Manually collect files to reuse ingest_files
            files = []
            for root, dirs, fnames in os.walk(folder):
                for f in fnames:
                    if f.lower().endswith(('.pdf','.txt','.docx')):
                        files.append(os.path.join(root, f))
            if files:
                ingest_files(files, cat)
            else:
                print(f"No new files in {folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into OPCA")
    parser.add_argument("--files", nargs="+", help="List of file paths to ingest")
    parser.add_argument("--folder", help="Folder path to ingest all supported files")
    parser.add_argument("--category", default="incoming", help="Category tag (default: incoming)")
    args = parser.parse_args()

    if args.files:
        ingest_files(args.files, args.category)
    elif args.folder:
        ingest_folder(args.folder, args.category)
    else:
        # Default: scan the three standard data folders
        ingest_default_folders()
    print("Ingestion process finished.")
