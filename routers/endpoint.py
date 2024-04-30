import asyncio
from typing import Union
import vertexai
import google.generativeai as gemini_client
from fastapi import HTTPException,APIRouter
from vertexai.generative_models import GenerativeModel
from typing import Union
from models.rag import rag

router= APIRouter()

# Defining a POST route /ask
@router.post("/ask")  
async def ask(question: Union[str, dict]): 

    qdrant_client=rag()
    # Checking if rag function returns True    
    
        
    try:
        search_result = qdrant_client.search(
            collection_name="my_collection",
            query_vector=gemini_client.embed_content(
                model="models/embedding-001",
                content=question,
                task_type="retrieval_query",
                ).get("embedding"),limit=3
            )

            # Processing search results and extracting text content
        data = []
        for result in search_result:
            content = {
                "id": result.id,
                "version": result.version,
                "score": result.score,
                "payload": result.payload,
                "vector": result.vector,
                "shard_key": result.shard_key
                }
            data.append(content)
 

            # Extracting text content from search results
        text_contents = []
        for item in data:
           text_contents.append(item['payload']['text'])
                
        prompt = f"Question: {question}\nContext: {' '.join(text_contents)}\n"
        print(prompt)
   
        # Initializing a Vertex AI project and a GenerativeModel instance
        vertexai.init(project='gemini-api-1234', location='us-central1')
        multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

        # Generating a response asynchronously using the extracted text content
        response = await asyncio.to_thread(multimodal_model.generate_content, prompt)
            
            
        final_data= response.text.replace("**", "").replace("*", "").replace("`", "").replace("\n", " ")
        return {"answer":final_data}

        

    except asyncio.TimeoutError:
        #Raise an HTTPException with status code 504 (Gateway Timeout) and a custom message
        raise HTTPException(status_code=504, detail="The response generation timed out.")
   
    








