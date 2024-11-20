from chromadb.api.segment import API
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from ..constants import CHROMA_SETTINGS


class RetrieverManager:
    def __init__(self, persist_directory: str, embeddings_model_name: str, target_source_chunks: int):
        self.persist_directory = persist_directory
        self.embeddings_model_name = embeddings_model_name
        self.target_source_chunks = target_source_chunks
        self.chroma_client = API.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings,
            client_settings=CHROMA_SETTINGS,
            client=self.chroma_client
        )

    def get_retriever(self):
        return self.vectorstore.as_retriever(search_kwargs={"k": self.target_source_chunks})

# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from chromadb.api.segment import ServerAPI  # Replace API with ServerAPI
# from ..constants import CHROMA_SETTINGS
#
# class RetrieverManager:
#     def __init__(self, persist_directory: str, embeddings_model_name: str, target_source_chunks: int):
#         self.persist_directory = persist_directory
#         self.embeddings_model_name = embeddings_model_name
#         self.target_source_chunks = target_source_chunks
#
#         self.chroma_client = ServerAPI(settings=CHROMA_SETTINGS)
#
#         self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
#
#         self.vectorstore = Chroma(
#             persist_directory=persist_directory,
#             embedding_function=self.embeddings,
#             client_settings=CHROMA_SETTINGS,
#             client=self.chroma_client
#         )
#
#     def get_retriever(self):
#         return self.vectorstore.as_retriever(search_kwargs={"k": self.target_source_chunks})