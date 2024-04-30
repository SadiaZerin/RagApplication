1. Created Environment
2. Imports necessary modules and classes and used fastapi for work
3. initializes QdrantClient instance with API key and URL and gemini client in settings.py.
4. created main.py for routing to any other endpoints.
5. Defines a function named rag() to perform the following operations:Creates a Qdrant collection named "my_collection" with specified vector configuration,Reads data from a file named 'data.txt',
   Splits the text into chunks using a RecursiveCharacterTextSplitter,Processes each chunk, embeds content using the Gemini client, and generates a unique ID for each point,Appends each point (consisting of ID, embeddings, and payload) to a list,
   Upserts the points to the Qdrant collection named "my_collection". As it is creating vector database, so it is in models file.
6. endpoint.py will start to excecute.The following operations are searching for content in a Qdrant collection using Gemini's embed_content function and Qdrant's search function,processing search results and extracting text content,Extracting text content from search results,
   Initializing a Vertex AI project and a GenerativeModel instance,Generating a response asynchronously using the extracted text content.
7. created dockerfile to build image.
8. The Docker Compose file defines a service named 'web', which will build an image using the Dockerfile in the current context and run it.

