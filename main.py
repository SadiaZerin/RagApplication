from fastapi import Depends, FastAPI
from qdrant_client import QdrantClient
import google.generativeai as gemini_client
import os
from routers import endpoint
from services.settings import initialize

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(endpoint.router)







