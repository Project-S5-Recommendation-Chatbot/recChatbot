#!/usr/bin/env python3

import time
from llm.llm_manager import LLMManager
from llm.query_handler import QueryHandler
from llm.utils import parse_arguments
from llm.retriever_manager import RetrieverManager


def main():

    args = parse_arguments()

    # Initialize components
    retriever_manager = RetrieverManager()
    retriever = retriever_manager.get_retriever()
    llm = LLMManager(args).get_llm()
    query_handler = QueryHandler(llm, retriever, args)

    # Interactive Q&A loop
    while True:
        query = input("\nEnter a query: ")
        if query.lower() == "exit":
            break
        if query.strip() == "":
            continue

        # Handle the query
        start = time.time()
        answer, sources = query_handler.handle_query(query)
        end = time.time()

        # Print the result
        print("\n\n> Question:")
        print(query)
        print(f"\n> Answer (took {round(end - start, 2)} s.):")
        print(answer)

        # Print sources if enabled
        for source in sources:
            print("\n> " + source["source"] + ":")
            print(source["content"])


if __name__ == "__main__":
    main()
