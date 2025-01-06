from typing import List  # For type hinting

from langchain.docstore.document import Document  # Document object for processing
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For splitting text into chunks


# Class for splitting documents into smaller chunks
class DocumentSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the DocumentSplitter with chunk size and overlap.
        :param chunk_size: The size of each chunk of text
        :param chunk_overlap: The number of overlapping characters between chunks
        """
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split a list of documents into smaller chunks.
        :param documents: A list of Document objects to split
        :return: A list of split Document objects
        """
        return self.splitter.split_documents(documents)  # Use RecursiveCharacterTextSplitter to split documents
