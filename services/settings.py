from qdrant_client import QdrantClient
import google.generativeai as gemini_client
import os

def initialize():
    gemini = "/run/secrets/gemini_api_key"
    qdrant = "/run/secrets/qdrant_api_key"
    
    with open(qdrant, "r") as qdrant_file:
        qdrant_api_key = qdrant_file.read().strip()
    with open(gemini, "r") as gemini_file:
        gemini_api_key = gemini_file.read().strip()

    qdrant_client = QdrantClient(
        api_key=qdrant_api_key,
        url="https://abccd4fc-ef32-480d-a818-533278db4c01.us-east4-0.gcp.cloud.qdrant.io"
    )

    gemini_client.configure(api_key=gemini_api_key)

    return qdrant_client, gemini_client

