import os
from typing import List
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from constants import CHROMA_SETTINGS
import chromadb
from langchain.docstore.document import Document

class VectorStoreHandler:
    def __init__(self, persist_directory: str, embeddings_model_name: str):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        self.chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)

    def does_vectorstore_exist(self) -> bool:
        db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        return bool(db.get()['documents'])

    def get_vectorstore(self) -> Chroma:
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            client_settings=CHROMA_SETTINGS,
            client=self.chroma_client
        )

    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        return Chroma.from_documents(
            documents,
            self.embeddings,
            persist_directory=self.persist_directory,
            client_settings=CHROMA_SETTINGS,
            client=self.chroma_client
        )
