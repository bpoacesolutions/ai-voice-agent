from fastapi import FastAPI
from pydantic import BaseModel

import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from fastapi.middleware.cors import CORSMiddleware

from app.memory_store import MemoryStore

from app.user_profile import UserProfile

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
memory_store = MemoryStore()

conversation_history = []

#user profile
user_profile = UserProfile()

# ---- Request schema ----
class QueryRequest(BaseModel):
    query: str


def extract_user_info(text: str):
    text = text.lower()
    info = {}

    # --- pets ---
    if "cat" in text:
        if "three" in text or "3" in text:
            info["cats"] = 3

    if "dog" in text:
        if "one" in text or "1" in text:
            info["dogs"] = 1

    if "fish" in text:
        if "one" in text or "1" in text:
            info["fish"] = 1

    # --- hobbies ---
    if "fishing" in text:
        info["hobby"] = "fishing"

    return info


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
    relevant_memory = memory_store.search(query, k=3)

    # ---- Context ----
    context = "\n".join(relevant_memory)
    history_text = "\n".join(conversation_history[-4:])

    # ---- Extract structured info ----
    extracted_info = extract_user_info(query)
    user_profile.update(extracted_info)

    profile_context = user_profile.get_context()

    # ---- Prompt ----
    prompt = f"""
You are a helpful AI assistant.

User profile:
{profile_context}

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

    #---- store conversation into memory ---#
    memory_store.add(f"User: {query}")
    memory_store.add(f"Agent: {answer}")

    # ---- Update history ----
    conversation_history.append(f"User: {query}")
    conversation_history.append(f"Agent: {answer}")

    return {
        "query": query,
        "response": answer,
        "memory_used": relevant_memory
    }