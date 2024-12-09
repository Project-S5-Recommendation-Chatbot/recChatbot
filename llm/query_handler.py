from langchain.chains import RetrievalQA  # For setting up a retrieval-based QA chain

# Class to handle queries using a language model (LLM) and a retriever
class QueryHandler:
    def __init__(self, llm, retriever, args):
        """
        Initialize QueryHandler with LLM, retriever, and arguments.
        :param llm: The language model (LLM) to use for answering queries
        :param retriever: The retriever to fetch relevant documents for the query
        :param args: Command-line arguments (to configure source document visibility)
        """
        # Create a RetrievalQA chain using the provided LLM and retriever
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,  # Language model to generate answers
            chain_type="stuff",  # Type of chain to use (stuffing documents into the prompt)
            retriever=retriever,  # Retriever to fetch relevant documents
            return_source_documents=not args.hide_source  # Optionally return source documents
        )
        self.hide_source = args.hide_source  # Store whether to hide source documents

    def handle_query(self, query):
        """
        Handle the user's query by passing it through the QA chain.
        :param query: The query to answer
        :return: The generated answer to the query
        """
        result = self.qa_chain(query)  # Get the result from the QA chain
        answer = result['result']  # Extract the answer from the result
        return answer  # Return the answer
