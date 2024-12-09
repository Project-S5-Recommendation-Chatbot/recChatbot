import os  # For file operations
from typing import List  # For type hinting
from langchain.document_loaders import *  # Import document loaders from langchain
from langchain.docstore.document import Document  # Document object for further processing

# Custom loader for email files, which falls back to loading text/plain content if HTML is not found
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work."""
    def load(self) -> List[Document]:
        try:
            try:
                doc = super().load()  # Try loading as normal email
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    self.unstructured_kwargs["content_source"] = "text/plain"  # Fallback to plain text
                    doc = super().load()  # Try loading plain text
                else:
                    raise  # Reraise the exception if not related to missing HTML
        except Exception as e:
            raise type(e)(f"{self.file_path}: {e}") from e  # Raise exception with file path context
        return doc  # Return the loaded document

# Mapping of file extensions to their respective loaders
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".eml": (MyElmLoader, {}),  # Use custom email loader
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}

def load_single_document(file_path: str) -> List[Document]:
    """
    Load a document based on its file extension using the appropriate loader.
    :param file_path: Path to the file to load
    :return: List of Document objects
    """
    ext = "." + file_path.rsplit(".", 1)[-1].lower()  # Extract the file extension
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]  # Get the loader class and its arguments
        loader = loader_class(file_path, **loader_args)  # Initialize the loader with the file path and args
        return loader.load()  # Load and return the document(s)
    raise ValueError(f"Unsupported file extension '{ext}'")  # Raise error if extension is not supported
