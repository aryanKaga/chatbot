from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio
import os
import certifi
import time

os.environ["SSL_CERT_FILE"] = certifi.where()
import ollama
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load vector store and embedding model
embedding_model=HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en",
    encode_kwargs={"normalize_embedding": True},
    
)
vectorstore=FAISS.load_local('rag_db',embedding_model,allow_dangerous_deserialization=True)




# Helper function to build message structure
def build_messages(prompt, retrieved_context):
    system_message = (
        "You are a helpful Woxsen university assistant that can answer questions about the context provided.\n\n"
        f"Context:\n{retrieved_context}"
    )
    return [{"role": "system", "content": system_message}] + [{"role": "user", "content": prompt}]

# Main chat endpoint
@app.get("/chat")
async def chat(question: str):
    # Retrieve top 3 relevant chunks for current question
    retrieved_docs = vectorstore.similarity_search(question,k=3)
    retrieved_context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    print(retrieved_docs)
    
    


    # Build complete messages for Ollama
    messages = build_messages(question, retrieved_context)

    # Print question to terminal
    print(f"\nUser Question: {question}")
    print("Assistant Response:", end=" ", flush=True)

    # Async generator for streaming
    async def generate_stream():
        for chunk in ollama.chat(model="llama3.2", messages=messages, stream=True):
            content = chunk['message']['content'].replace("\n","<br>")
            if content:
                print(content, end="", flush=False)
                yield f"data: {content}\n\n"
        yield "event: end\ndata: \n\n" # Signal the end of the stream

    return StreamingResponse(generate_stream(), media_type="text/event-stream")
