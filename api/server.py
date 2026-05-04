from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import requests

from app.memory_store import MemoryStore

# ---- Setup ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"

# ---- Memory ----
memory_store = MemoryStore()
conversation_history = []

# ---- Request schema ----
class QueryRequest(BaseModel):
    query: str


# ---- Memory Summarizer ----
def summarize_memory(query, answer):
    prompt = f"""
Extract key facts about the user from this conversation.

Focus on durable information (things that remain true over time).
Avoid conversational phrases.

Examples:
- User owns 3 cats
- User works as a developer
- User lives in Paris

Conversation:
User: {query}
Agent: {answer}

Facts:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json().get("response", "").strip()


# ---- API Endpoint ----
@app.post("/ask")
def ask_agent(request: QueryRequest):
    query = request.query

    # ---- Retrieve memory (vector search) ----
    raw_memory = memory_store.search(query, k=6)

    # ---- Filter memory (lower distance = better) ----
    filtered_memory = [
        text for text, score in raw_memory if score < 1.5
    ]

    # fallback if filtering too aggressive
    if not filtered_memory:
        filtered_memory = [text for text, _ in raw_memory[:3]]

    # ---- Context ----
    context = "\n".join(filtered_memory)
    history_text = "\n".join(conversation_history[-4:])

    # ---- Prompt (IMPROVED) ----
    prompt = f"""
You are a helpful AI assistant.

Use ALL available information to answer accurately.

Memory (past facts):
{context}

Recent conversation:
{history_text}

Instructions:
- Use memory when relevant
- If the user asks about past facts, rely on memory
- If multiple facts exist, combine them logically
- Do NOT say "I don't know" if the answer exists in memory

User question:
{query}

Answer:
"""

    # ---- LLM Call ----
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        answer = response.json().get("response", "Error: no response from model")

    except Exception as e:
        print("LLM call failed:", e)
        answer = "Error: LLM service unavailable"

    # ---- Store raw conversation ----
    memory_store.add(f"User: {query}")
    memory_store.add(f"Agent: {answer}")

    # ---- Store enriched memory ----
    try:
        summary = summarize_memory(query, answer)

        facts = [
            f.strip("- ").strip()
            for f in summary.split("\n")
            if f.strip()
        ]

        for fact in facts:
            # keep only meaningful user facts
            if len(fact) > 10 and "user" in fact.lower():
                memory_store.add(fact)

    except Exception as e:
        print("Memory summarization failed:", e)

    # ---- Update history ----
    conversation_history.append(f"User: {query}")
    conversation_history.append(f"Agent: {answer}")

    return {
        "query": query,
        "response": answer,
        "memory_used": filtered_memory
    }