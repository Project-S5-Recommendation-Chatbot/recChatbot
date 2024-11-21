from langchain.chains import RetrievalQA


class QueryHandler:
    def __init__(self, llm, retriever, args):
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=not args.hide_source
        )
        self.hide_source = args.hide_source

    def handle_query(self, query):
        result = self.qa_chain(query)
        answer = result['result']
        sources = []
        if not self.hide_source:
            sources = [{"source": doc.metadata["source"], "content": doc.page_content} for doc in result['source_documents']]
        return answer, sources
