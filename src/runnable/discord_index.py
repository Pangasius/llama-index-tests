# package: code/tests

from llama_index import GPTVectorStoreIndex, download_loader

from llama_index.indices.service_context import ServiceContext

from backend.model import ModelLLM

import os
from dotenv import load_dotenv

class DiscordReader:
    def __init__(self):
        #import discord token from .env
        load_dotenv()

        self.discord_token = os.getenv("DISCORD_TOKEN")
        
        self.query_engine = None
        
        self.load_data()
    
    def load_data(self, channel_ids=[1138109436750221375], llm=ModelLLM(), embed_model="local"):
        
        DiscordReader = download_loader('DiscordReader')

        reader = DiscordReader(discord_token=self.discord_token)
        documents = reader.load_data(channel_ids=channel_ids)

        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

        print("Indexing documents...")

        self.query_engine = index.as_query_engine(service_context=service_context)

        print("Indexing complete. Ready to query.")
        
    def query(self, query):
        return self.query_engine.query(query)

def run_discord_index():
    DiscordReader()
    
    while True:
        query = input("Query: ")
        answer = DiscordReader().query(query)
        
        print(f"Query: {query}")
        print(f"Answer: {answer}")
        print(f"Sources: {answer.get_formatted_sources()}")
