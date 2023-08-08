from llama_index import GPTVectorStoreIndex, download_loader, SimpleDirectoryReader

from llama_index.indices.service_context import ServiceContext

import os
from dotenv import load_dotenv

from model import ModelLLM

load_dotenv()

#DiscordReader = download_loader('DiscordReader')

#discord_token = os.getenv("DISCORD_TOKEN")

#channel_ids = [1138109436750221375]  # Replace with your channel_id
#reader = DiscordReader(discord_token=discord_token)
#documents = reader.load_data(channel_ids=channel_ids)

documents = SimpleDirectoryReader("examples/F12-FR/", recursive=True).load_data()

llm = ModelLoader.

service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")

index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

print("Indexing documents...")

query_engine = index.as_query_engine(service_context=service_context, verbose=True)

print("Indexing complete. Ready to query.")

query = "Give the number of files mentioned in the channel."
answer = query_engine.query(query)

print(f"Query: {query}")
print(f"Answer: {answer}")
print(f"Sources: {answer.get_formatted_sources()}")