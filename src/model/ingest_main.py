import os
from dotenv import load_dotenv
from document_processor import process_documents
from vectorstore_manager import does_vectorstore_exist, batch_chromadb_insertions
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from constants import CHROMA_SETTINGS

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

persist_directory = os.environ.get('PERSIST_DIRECTORY')
source_directory = os.environ.get('SOURCE_DIRECTORY', 'source_documents')
embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')
chunk_size = 500
chunk_overlap = 50

def main():
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    documents = process_documents(source_directory, chunk_size, chunk_overlap)
    chroma_client = Chroma.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)

    if does_vectorstore_exist(persist_directory, embeddings):
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)
        for batch in batch_chromadb_insertions(chroma_client, documents):
            db.add_documents(batch)
    else:
        db = Chroma.from_documents(documents, embeddings, persist_directory=persist_directory, client_settings=CHROMA_SETTINGS, client=chroma_client)

    print("Ingestion complete!")

if __name__ == "__main__":
    main()
