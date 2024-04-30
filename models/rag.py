from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import Distance, PointStruct, VectorParams
from qdrant_client.models import Distance
import google.generativeai as gemini_client
from qdrant_client.models import PointStruct
import uuid
from services.settings import initialize

qdrant_client,gemini_client = initialize()

# Function to perform necessary operations (create collection, embed content, upsert points)
def rag():
        
        collection_name="my_collection"
        existing_collections = qdrant_client.get_collections()
        collection_names = [collection.name for collection in existing_collections.collections]
        if collection_name in collection_names:
            return True
        else:
            # Creating a Qdrant collection
            qdrant_client.create_collection(
                collection_name="my_collection",
                vectors_config=VectorParams(size=768,
                distance=Distance.COSINE))
           
        
        # Reading data from a file
        with open('txt_files/data.txt') as f:
            raw_text = f.read()

        text = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=100,
            length_function=len)
        
        # Splitting text into chunks
        chunks = text.split_text(raw_text)
        print(chunks)


        points = []
        # Processing chunks and embedding content
        for chunk in chunks:
            embedding_model = "models/embedding-001"
            result = gemini_client.embed_content(
                model=embedding_model,
                content=chunk,
                task_type="retrieval_document",
                title="Qdrant x Gemini")
            
            # Generating unique ID for each point
            point_id = str(uuid.uuid4())  
            embeddings = result['embedding']
            points.append(PointStruct(id=point_id, vector=embeddings,
            payload={"text": chunk}))
        

        # Upserting points to the Qdrant collection
        qdrant_client.upsert(
            collection_name="my_collection",
            wait=True,
            points=points)
        
        return qdrant_client
   

