import glob
import os
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
from ingestor.loaders import load_single_document
from ingestor.splitter import DocumentSplitter
from ingestor.loaders import LOADER_MAPPING
from langchain.docstore.document import Document

class DocumentIngestion:
    def __init__(self, source_directory: str, chunk_size: int, chunk_overlap: int):
        self.source_directory = source_directory
        self.splitter = DocumentSplitter(chunk_size, chunk_overlap)

    def load_documents(self, ignored_files: List[str] = []) -> List[Document]:
        all_files = []
        for ext in LOADER_MAPPING:
            all_files.extend(
                glob.glob(os.path.join(self.source_directory, f"**/*{ext.lower()}"), recursive=True)
            )
            all_files.extend(
                glob.glob(os.path.join(self.source_directory, f"**/*{ext.upper()}"), recursive=True)
            )
        filtered_files = [file for file in all_files if file not in ignored_files]

        with Pool(processes=os.cpu_count()) as pool:
            results = []
            with tqdm(total=len(filtered_files), desc='Loading documents', ncols=80) as pbar:
                for docs in pool.imap_unordered(load_single_document, filtered_files):
                    results.extend(docs)
                    pbar.update()
        return results

    def process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        documents = self.load_documents(ignored_files)
        if not documents:
            print("No new documents to load")
            exit(0)
        return self.splitter.split_documents(documents)
