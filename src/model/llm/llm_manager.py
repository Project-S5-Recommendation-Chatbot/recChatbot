from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp, GPT4All


class LLMManager:
    def __init__(self, model_type: str, model_path: str, model_n_ctx: int, model_n_batch: int, mute_stream: bool):
        self.model_type = model_type
        self.model_path = model_path
        self.model_n_ctx = model_n_ctx
        self.model_n_batch = model_n_batch
        self.callbacks = [] if mute_stream else [StreamingStdOutCallbackHandler()]

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
