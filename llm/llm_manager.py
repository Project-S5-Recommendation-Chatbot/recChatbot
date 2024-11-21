import os
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All, LlamaCpp


class LLMManager:
    def __init__(self, args):
        self.model_type = os.environ.get('MODEL_TYPE')
        self.model_path = os.environ.get('MODEL_PATH')
        self.model_n_ctx = os.environ.get('MODEL_N_CTX')
        self.model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))
        self.callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]

    def get_llm(self):
        match self.model_type:
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
                    backend='gptj',
                    n_batch=self.model_n_batch,
                    callbacks=self.callbacks,
                    verbose=False
                )
            case _:
                raise ValueError(f"Unsupported model type: {self.model_type}")
