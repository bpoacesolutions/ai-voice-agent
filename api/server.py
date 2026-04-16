from fastapi import FastAPI
from pydantic import BaseModel

import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from fastapi.middleware.cors import CORSMiddleware

# ---- Setup ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (fine for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
#embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_model = None
# ---- Memory ----
memory = [
    "User likes Italian food",
    "User prefers quick meals",
    "User goes to the gym regularly"
]

conversation_history = []

# ---- Request schema ----
class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_agent(request: QueryRequest):
    query = request.query

    #
    def get_model():
        global embedding_model
        if embedding_model is None:
            embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        return embedding_model
    
    model = get_model()

    # ---- Retrieve memory ----
    memory_embeddings = model.encode(memory)
    query_embedding = model.encode([query])

    scores = cosine_similarity(query_embedding, memory_embeddings)[0]
    top_indices = scores.argsort()[-2:][::-1]
    relevant_memory = [memory[i] for i in top_indices]

    # ---- Context ----
    context = "\n".join(relevant_memory)
    history_text = "\n".join(conversation_history[-4:])

    # ---- Prompt ----
    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Conversation history:
{history_text}

User question:
{query}

Answer:
"""

    # ---- LLM ----
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    answer = response.json()["response"]

    # ---- Update history ----
    conversation_history.append(f"User: {query}")
    conversation_history.append(f"Agent: {answer}")

    return {
        "query": query,
        "response": answer,
        "memory_used": relevant_memory
    }