import time
from langchain.chains import RetrievalQA

class QARunner:
    def __init__(self, retriever, llm, hide_source: bool):
        self.qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=not hide_source
        )
        self.hide_source = hide_source

    def start_interactive_loop(self):
        print("\nType 'exit' to quit the application.")
        while True:
            query = input("\nEnter a query: ")
            if query.lower() == "exit":
                break
            if not query.strip():
                continue

            start = time.time()
            res = self.qa(query)
            end = time.time()

            answer = res['result']
            docs = [] if self.hide_source else res['source_documents']

            print("\n\n> Question:")
            print(query)
            print(f"\n> Answer (took {round(end - start, 2)} s.):")
            print(answer)

            for document in docs:
                print("\n> Source: " + document.metadata["source"])
                print(document.page_content)
