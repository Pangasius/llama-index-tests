from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, download_loader

from llama_index.indices.service_context import ServiceContext

from model import ModelLLM

from singleton import Singleton

class QueryEngine(metaclass=Singleton):
    def __init__(self):
        
        llm = ModelLLM()
        service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")
        
        print("Indexing documents...")

        documents = SimpleDirectoryReader("examples/F12-FR/", recursive=True).load_data()
        
        #WikipediaReader = download_loader("WikipediaReader")

        #loader = WikipediaReader()
        #documents += loader.load_data(pages=["Électricité_de_France"])
        
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

        self.query_engine = index.as_query_engine(service_context=service_context, verbose=True)
        
        print("Indexing complete. Ready to query.")
        
    def query(self, query):
        return self.query_engine.query(query)
    
if __name__ == "__main__":
    q = QueryEngine()
    print(q.query("What type of conviction has EDF (Electrivité de France) received?"))