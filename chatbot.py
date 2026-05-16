from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("doctor_website")
groq_client = Groq(api_key="")

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    question_vector = embedding_model.encode([request.question])
    results = collection.query(
        query_embeddings=question_vector.tolist(),
        n_results=3
    )
    context = "\n\n".join(results['documents'][0])
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""Tu BrandGrowth agency ka assistant hai.
Sirf neeche diye context se jawab de.
Agar answer nahi mila: 'Contact karein: support@brandgrowth.tech'
Context: {context}"""
            },
            {
                "role": "user",
                "content": request.question
            }
        ]
    )
    return {"answer": response.choices[0].message.content}