import os  # For file and directory operations
from typing import List  # For type hinting
from langchain.vectorstores import Chroma  # For using Chroma vector store
from langchain.embeddings import HuggingFaceEmbeddings  # For embedding documents using HuggingFace model
from constants import CHROMA_SETTINGS  # Custom Chroma settings from constants file
import chromadb  # Client for interacting with Chroma database
from langchain.docstore.document import Document  # Document object for further processing

# Class to handle interactions with a Chroma vector store
class VectorStoreHandler:
    def __init__(self, persist_directory: str, embeddings_model_name: str):
        """
        Initialize VectorStoreHandler with persistence directory and embedding model.
        :param persist_directory: Path where the vector store data will be stored
        :param embeddings_model_name: Name of the HuggingFace model to use for embeddings
        """
        self.persist_directory = persist_directory  # Directory to persist vector store
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)  # Embeddings for documents
        self.chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)  # Chroma client

    def does_vectorstore_exist(self) -> bool:
        """
        Check if a vector store already exists in the given directory.
        :return: True if vector store exists, False otherwise
        """
        db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        return bool(db.get()['documents'])  # Check if there are any documents in the vector store

    def get_vectorstore(self) -> Chroma:
        """
        Get the Chroma vector store client.
        :return: Chroma vector store client
        """
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            client_settings=CHROMA_SETTINGS,
            client=self.chroma_client
        )

    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Create a new Chroma vector store from a list of documents.
        :param documents: List of Document objects to index
        :return: Chroma vector store client
        """
        return Chroma.from_documents(
            documents,
            self.embeddings,
            persist_directory=self.persist_directory,
            client_settings=CHROMA_SETTINGS,
            client=self.chroma_client
        )
