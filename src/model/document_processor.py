import os
import glob
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from loaders import load_single_document, LOADER_MAPPING

def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext.lower()}"), recursive=True)
        )
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext.upper()}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for docs in pool.imap_unordered(load_single_document, filtered_files):
                results.extend(docs)
                pbar.update()
    return results

def process_documents(source_directory: str, chunk_size: int, chunk_overlap: int, ignored_files: List[str] = []) -> List[Document]:
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        raise ValueError("No new documents to load")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)
