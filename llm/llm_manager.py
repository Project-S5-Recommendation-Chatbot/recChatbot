import os  # For accessing environment variables
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler  # For streaming model output to stdout
from langchain.llms import GPT4All, LlamaCpp  # For loading GPT4All and LlamaCpp models

# Class for managing language model (LLM) setup and instantiation
class LLMManager:
    def __init__(self, args):
        """
        Initialize the LLMManager with configuration from environment variables and command-line arguments.
        :param args: Command-line arguments (used to mute streaming output if needed)
        """
        self.model_type = os.environ.get('MODEL_TYPE')  # Get model type (e.g., LlamaCpp, GPT4All)
        self.model_path = os.environ.get('MODEL_PATH')  # Path to the model
        self.model_n_ctx = os.environ.get('MODEL_N_CTX')  # Context size for the model
        self.model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))  # Batch size for model inference (default 8)
        self.callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]  # Optional stdout streaming

    def get_llm(self):
        """
        Return the appropriate language model based on the model type.
        :return: Language model instance (LlamaCpp or GPT4All)
        """
        match self.model_type:  # Match model type
            case "LlamaCpp":
                return LlamaCpp(
                    model_path=self.model_path,
                    max_tokens=self.model_n_ctx,
                    n_batch=self.model_n_batch,
                    callbacks=self.callbacks,
                    verbose=False
                )
            case "GPT4All":
                return GPT4All(
                    model=self.model_path,
                    max_tokens=self.model_n_ctx,
                    backend='gptj',  # Set GPTJ as the backend for GPT4All
                    n_batch=self.model_n_batch,
                    callbacks=self.callbacks,
                    verbose=False
                )
            case _:
                raise ValueError(f"Unsupported model type: {self.model_type}")  # Raise error for unsupported model types
