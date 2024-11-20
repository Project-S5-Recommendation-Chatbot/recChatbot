import os
from dotenv import load_dotenv
from argparse import ArgumentParser
from retriever import RetrieverManager
from llm_manager import LLMManager
from qa_runner import QARunner

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)


def parse_arguments():
    parser = ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection.')
    parser.add_argument("--hide-source", "-S", action='store_true', help="Disable printing source documents.")
    parser.add_argument("--mute-stream", "-M", action='store_true', help="Disable streaming output from the LLM.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    persist_directory = os.getenv('PERSIST_DIRECTORY')
    embeddings_model_name = os.getenv('EMBEDDINGS_MODEL_NAME')
    model_type = os.getenv('MODEL_TYPE')
    model_path = os.getenv('MODEL_PATH')
    model_n_ctx = int(os.getenv('MODEL_N_CTX', 2048))
    model_n_batch = int(os.getenv('MODEL_N_BATCH', 8))
    target_source_chunks = int(os.getenv('TARGET_SOURCE_CHUNKS', 4))

    # Initialize Retriever
    retriever_manager = RetrieverManager(
        persist_directory=persist_directory,
        embeddings_model_name=embeddings_model_name,
        target_source_chunks=target_source_chunks
    )
    retriever = retriever_manager.get_retriever()

    # Initialize LLM
    llm_manager = LLMManager(
        model_type=model_type,
        model_path=model_path,
        model_n_ctx=model_n_ctx,
        model_n_batch=model_n_batch,
        mute_stream=args.mute_stream
    )
    llm = llm_manager.get_llm()

    # Run QA Loop
    qa_runner = QARunner(retriever, llm, hide_source=args.hide_source)
    qa_runner.start_interactive_loop()


if __name__ == "__main__":
    main()
