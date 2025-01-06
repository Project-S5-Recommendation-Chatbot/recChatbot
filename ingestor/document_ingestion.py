import glob  # For finding files matching a pattern
import os  # For file and directory operations
from multiprocessing import Pool  # For parallel processing
from typing import List  # For type hinting

from langchain.docstore.document import Document  # Document object for further processing

from ingestor.loaders import LOADER_MAPPING  # Mapping of file extensions to loaders
from ingestor.loaders import load_single_document  # Function to load a single document
from ingestor.splitter import DocumentSplitter  # For splitting documents into chunks


# Class for ingesting and processing documents from a source directory
class DocumentIngestion:
    def __init__(self, source_directory: str, chunk_size: int, chunk_overlap: int):
        """
        Initialize the DocumentIngestion instance.
        :param source_directory: Path to the directory containing source documents
        :param chunk_size: Size of each document chunk
        :param chunk_overlap: Overlap between consecutive chunks
        """
        self.source_directory = source_directory  # Directory with documents to process
        self.splitter = DocumentSplitter(chunk_size, chunk_overlap)  # Initialize splitter

    def load_documents(self, ignored_files: List[str] = []) -> List[Document]:
        """
        Load documents from the source directory.
        :param ignored_files: List of file paths to ignore
        :return: List of loaded Document objects
        """
        all_files = []  # List to hold all matching file paths

        # Find all files matching the extensions in LOADER_MAPPING
        for ext in LOADER_MAPPING:
            all_files.extend(
                glob.glob(os.path.join(self.source_directory, f"**/*{ext.lower()}"), recursive=True)
            )
            all_files.extend(
                glob.glob(os.path.join(self.source_directory, f"**/*{ext.upper()}"), recursive=True)
            )

        # Filter out ignored files
        filtered_files = [file for file in all_files if file not in ignored_files]

        with Pool(processes=os.cpu_count()) as pool:  # Use parallel processing
            results = []
            for docs in pool.imap_unordered(load_single_document, filtered_files):  # Load documents
                results.extend(docs)
        return results  # Return all loaded documents

    def process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        """
        Process documents by splitting them into smaller chunks.
        :param ignored_files: List of file paths to ignore
        :return: List of processed Document objects
        """
        documents = self.load_documents(ignored_files)  # Load documents from source
        return self.splitter.split_documents(documents)  # Split documents into chunks
