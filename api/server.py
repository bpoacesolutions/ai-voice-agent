from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import requests

from app.memory_store import MemoryStore

from app.brain import AgentBrain

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
brain = AgentBrain(memory_store)
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

    # ---- Brain Retrieval ----
    filtered_memory = brain.retrieve_memory(query)

    # ---- Context ----
    context = "\n".join(filtered_memory)
    history_text = "\n".join(conversation_history[-4:])

    # ---- Prompt (IMPROVED) ----
    prompt = brain.build_prompt(
        query=query,
        memory=filtered_memory,
        history=conversation_history
    )

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
    memory_store.add(
        f"User: {query}",
        memory_type="conversation"
    )

    memory_store.add(
        f"Agent: {answer}",
        memory_type="conversation"
    )

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
                memory_store.add(
                    fact,
                    memory_type="fact"
                )

    except Exception as e:
        print("Memory summarization failed:", e)

    # ---- Generate Reflection Memory ----
    fact_count = len([
        m for m in memory_store.texts
        if m["type"] == "fact"
    ])

    if fact_count >= 4 and fact_count % 4 == 0:
        try:
            recent_memories = [
                m["text"]
                for m in memory_store.texts[-8:]
                if m["type"] == "fact"
            ]

            reflection = generate_reflection(recent_memories)

            reflections = [
                r.strip("- ").strip()
                for r in reflection.split("\n")
                if r.strip()
            ]

            for reflection in reflections:

                if brain.validate_reflection(reflection):

                    memory_store.add(
                        reflection,
                        memory_type="reflection"
                    )

                else:
                    print(f"⚠️ Rejected weak reflection: {reflection}")

        except Exception as e:
            print("Reflection generation failed:", e)    

    # ---- Update history ----
    conversation_history.append(f"User: {query}")
    conversation_history.append(f"Agent: {answer}")

    return {
        "query": query,
        "response": answer,
        "memory_used": filtered_memory
    }


@app.post("/reset")
def reset_memory():
    global conversation_history

    memory_store.reset()
    conversation_history = []

    return {"status": "memory_cleared"}


def generate_reflection(memories):
    joined_memories = "\n".join(memories)

    prompt = f"""
You are generating high-level reflections
about a user based on long-term memories.

Memories:
{joined_memories}

Generate ONLY short durable reflections.

Rules:
- One reflection per line
- Keep them short
- No explanations
- No numbering
- No intro sentence
- No speculative psychology
- Avoid weak guesses

Good Examples:
- User is an animal lover
- User enjoys active hobbies
- User values companionship

Bad Examples:
- User probably values work-life balance
- The user may possibly enjoy...

Reflections:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()