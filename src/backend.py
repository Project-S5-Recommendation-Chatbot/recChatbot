import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from model.ingestor.document_processor import process_documents
from model.llm.llm_manager import LLMManager
from model.llm.retriever import RetrieverManager
from langchain.chains import RetrievalQA

if not load_dotenv():
    raise RuntimeError("Could not load .env file. Ensure it exists and is readable.")

app = Flask(__name__)

PERSIST_DIRECTORY = os.getenv('PERSIST_DIRECTORY')
EMBEDDINGS_MODEL_NAME = os.getenv('EMBEDDINGS_MODEL_NAME')
MODEL_TYPE = os.getenv('MODEL_TYPE')
MODEL_PATH = os.getenv('MODEL_PATH')
MODEL_N_CTX = int(os.getenv('MODEL_N_CTX', 2048))
MODEL_N_BATCH = int(os.getenv('MODEL_N_BATCH', 8))
TARGET_SOURCE_CHUNKS = int(os.getenv('TARGET_SOURCE_CHUNKS', 4))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 500))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))

try:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
    retriever_manager = RetrieverManager(
        persist_directory=PERSIST_DIRECTORY,
        embeddings_model_name=EMBEDDINGS_MODEL_NAME,
        target_source_chunks=TARGET_SOURCE_CHUNKS
    )
    retriever = retriever_manager.get_retriever()

    llm_manager = LLMManager(
        model_type=MODEL_TYPE,
        model_path=MODEL_PATH,
        model_n_ctx=MODEL_N_CTX,
        model_n_batch=MODEL_N_BATCH,
        mute_stream=True
    )
    llm = llm_manager.get_llm()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
except Exception as e:
    raise RuntimeError(f"Error initializing components: {e}")


@app.route("/query", methods=["POST"])
def handle_query():
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()
        if not user_query:
            return jsonify({"error": "Query cannot be empty"}), 400

        retrieval_result = retriever.get_relevant_documents(user_query)
        if not retrieval_result:
            return jsonify({"error": "No relevant documents found"}), 404

        processed_documents = process_documents(
            source_directory=PERSIST_DIRECTORY,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            ignored_files=[]
        )

        result = qa_chain(user_query)

        answer = result.get("result", "No answer generated.")
        source_docs = result.get("source_documents", [])

        response = {
            "query": user_query,
            "answer": answer,
            "sources": [
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "content": doc.page_content
                } for doc in source_docs
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
