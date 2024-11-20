from typing import List
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from chromadb.api.segment import API

def does_vectorstore_exist(persist_directory: str, embeddings: HuggingFaceEmbeddings) -> bool:
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return bool(db.get()['documents'])

def batch_chromadb_insertions(chroma_client: API, documents: List[Document]) -> List[Document]:
    max_batch_size = chroma_client.max_batch_size
    for i in range(0, len(documents), max_batch_size):
        yield documents[i:i + max_batch_size]
