import asyncio
import os
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient

async def main():
    load_dotenv()
    print("Connecting to Qdrant Cloud...")
    
    # Connect directly using your environment variables
    client = AsyncQdrantClient(
        url=os.getenv("QDRANT_URL"), 
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    print("Forcing keyword index for 'deal_id'...")
    await client.create_payload_index(
        collection_name="startup_website_chunks",
        field_name="deal_id",
        field_schema="keyword"
    )
    
    print("Forcing keyword index for 'category'...")
    await client.create_payload_index(
        collection_name="startup_website_chunks",
        field_name="category",
        field_schema="keyword"
    )
    
    print("SUCCESS! The database strict-mode is satisfied.")

asyncio.run(main())