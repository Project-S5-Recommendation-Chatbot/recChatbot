import os

import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from constants import CHROMA_SETTINGS


class RetrieverManager:
    def __init__(self):
        self.embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
        self.persist_directory = os.environ.get('PERSIST_DIRECTORY')
        self.target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))

    def get_retriever(self):
        embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_model_name)
        chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=self.persist_directory)
        db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings,
            client_settings=CHROMA_SETTINGS,
            client=chroma_client
        )
        return db.as_retriever(search_kwargs={"k": self.target_source_chunks})