#!/usr/bin/env python3
import os
from ingestor.vectorstore import VectorStoreHandler
from ingestor.document_ingestion import DocumentIngestion

def main():
    source_directory = os.getenv("SOURCE_DIRECTORY", "source_documents")
    persist_directory = os.getenv("PERSIST_DIRECTORY")
    embeddings_model_name = os.getenv("EMBEDDINGS_MODEL_NAME")
    chunk_size = int(os.getenv("CHUNK_SIZE", 500))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 50))

    vectorstore = VectorStoreHandler(persist_directory, embeddings_model_name)
    ingestion = DocumentIngestion(source_directory, chunk_size, chunk_overlap)

    if vectorstore.does_vectorstore_exist():
        print(f"Appending to existing vectorstore at {persist_directory}")
        documents = ingestion.process_documents()
        db = vectorstore.get_vectorstore()
        db.add_documents(documents)
    else:
        print("Creating new vectorstore")
        documents = ingestion.process_documents()
        vectorstore.create_vectorstore(documents)

    print("Ingestion complete!")

if __name__ == "__main__":
    main()
