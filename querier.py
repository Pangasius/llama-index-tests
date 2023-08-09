from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, download_loader

from llama_index.indices.service_context import ServiceContext
from llama_index.indices.prompt_helper import PromptHelper

from model import ModelLLM, ModelLoader, Embedding

from singleton import Singleton

class QueryEngine(metaclass=Singleton):
    def __init__(self):
        
        prompt_helper = PromptHelper(chunk_overlap_ratio=0.2,
                                     tokenizer=ModelLoader().tokenizer,
                                     chunk_size_limit=512,
                                     context_window=1024)
        
        llm = ModelLLM()
        embedder = "local" #Embedding()
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embedder, prompt_helper=prompt_helper)
        
        print("Indexing documents...")

        WikipediaReader = download_loader("WikipediaReader")
        loader = WikipediaReader()
        documents = loader.load_data(pages=["Électricité_de_France", "France", "Electricity pricing"])
        
        documents += SimpleDirectoryReader("examples/F12-FR/available/", recursive=True).load_data()
        
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

        self.query_engine = index.as_query_engine(service_context=service_context)
        
        print("Indexing complete. Ready to query.")
        
    def query(self, query):
        return self.query_engine.query(query)
    
if __name__ == "__main__":
    q = QueryEngine()
    print(q.query("What type of conviction has EDF (Electrivité de France) received?"))