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
                    max_tokens=200,  # Reduces verbosity
                    n_ctx=4096,  # Maintains context window
                    n_batch=16,  # Balances latency and performance
                    callbacks=self.callbacks,
                    verbose=True,  # Enables debugging
                    n_threads=128,  # Matches hardware capabilities
                    n_gpu_layers=8,  # Optimizes GPU usage
                    temperature=0.6,  # Encourages determinism
                    top_p=0.8,  # Balances creativity and focus
                    repeat_penalty=1.5,  # Discourages repetitive content
                    presence_penalty=0.8,  # Encourages new ideas
                    # frequency_penalty=0.6,  # Reduces overused phrases
                    stop_sequences=[
                        "\n", "I don't know", "I'm just telling you",
                        "don't", "note:", "(note:)", "answer", "unhelpful", "i", "useless", "note",
                        "not-so-helpful", "not", "helpful", "limitation", "limitations", "seems", "please",
                        "unfortunately", "fortunately", "unfortunately,", "fortunately,", "however", "however,",
                        "since", "since,", "{", "}", "source", "source,", "source:","Question","question","Question:","question:"
                    ]
                )

            case "GPT4All":
                return GPT4All(
                    model=self.model_path,
                    max_tokens=4096,
                    backend='llama',  # Set GPTJ as the backend for GPT4All
                    n_batch=8,
                    callbacks=self.callbacks,
                    verbose=False,
                    n_threads=8,
                    n_predict=120,
                )
            case _:
                raise ValueError(
                    f"Unsupported model type: {self.model_type}")  # Raise error for unsupported model types
