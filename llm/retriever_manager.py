import os  # For accessing environment variables

import chromadb  # Client for interacting with Chroma database
from langchain.embeddings import HuggingFaceEmbeddings  # For using HuggingFace embeddings
from langchain.vectorstores import Chroma  # For interacting with Chroma vector store

from constants import CHROMA_SETTINGS  # Custom Chroma settings from constants file


# Class to manage the retriever setup for querying the vector store
class RetrieverManager:
    def __init__(self):
        """
        Initialize RetrieverManager with configuration from environment variables.
        """
        self.embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")  # Get the embeddings model name
        self.persist_directory = os.environ.get('PERSIST_DIRECTORY')  # Path where vector store is persisted
        self.target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))  # Number of source chunks for retrieval

    def get_retriever(self):
        """
        Create and return a retriever that interacts with the Chroma vector store.
        :return: A retriever for the Chroma vector store
        """
        embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_model_name)  # Initialize embeddings using HuggingFace model
        chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=self.persist_directory)  # Chroma client
        db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings,  # Use embeddings for the vector store
            client_settings=CHROMA_SETTINGS,
            client=chroma_client  # Client for accessing Chroma
        )
        return db.as_retriever(search_kwargs={"k": self.target_source_chunks})  # Return the retriever with target chunks for search
