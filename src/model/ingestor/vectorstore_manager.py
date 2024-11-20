from typing import List

from chromadb.api.segment import API
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


def does_vectorstore_exist(persist_directory: str, embeddings: HuggingFaceEmbeddings) -> bool:
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return bool(db.get()['documents'])

def batch_chromadb_insertions(chroma_client: API, documents: List[Document]) -> List[Document]:
    max_batch_size = chroma_client.max_batch_size
    for i in range(0, len(documents), max_batch_size):
        yield documents[i:i + max_batch_size]

# from typing import List, Generator
# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.docstore.document import Document
# from chromadb.api.segment import ServerAPI  # Using ServerAPI
#
#
# def does_vectorstore_exist(persist_directory: str, embeddings: HuggingFaceEmbeddings) -> bool:
#     db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
#     return bool(db.get()['documents'])
#
#
# def batch_chromadb_insertions(
#         chroma_client: ServerAPI,
#         documents: List[Document],
#         max_batch_size: int = 100
# ) -> Generator[List[Document], None, None]:
#     for i in range(0, len(documents), max_batch_size):
#         yield documents[i:i + max_batch_size]