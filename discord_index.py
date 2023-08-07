from llama_index import VectorStoreIndex, download_loader

import os
from dotenv import load_dotenv

from model import ModelLLM

load_dotenv()

DiscordReader = download_loader('DiscordReader')

discord_token = os.getenv("DISCORD_TOKEN")

channel_ids = [1138109436750221375]  # Replace with your channel_id
reader = DiscordReader(discord_token=discord_token)
documents = reader.load_data(channel_ids=channel_ids)

llm = ModelLLM()

service_context = {
    "llm": llm,
    }

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
query_engine.query("What is the latest post?")