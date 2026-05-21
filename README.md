# AI Voice Agent

## Overview

This project implements a modular AI agent capable of:

- understanding spoken or typed input
- retrieving contextual memory using vector search (FAISS)
- extracting durable facts from conversations
- generating higher-level reflections about the user
- building contextual prompts using layered memory
- generating responses using a local LLM
- replying through voice or browser chat interfaces

The system supports both:

- a Python voice client
- a browser-based conversational interface

The architecture is modular and designed to evolve toward a production-grade long-term memory AI system.

---

# Architecture

```text
Voice Client (app/)        OR        Web Interface (web/)
            ↓
        API Backend (api/)
            ↓
     Agent Brain Layer
            ↓
   Memory System (FAISS)
            ↓
     LLM Service (Ollama)
```

---

# Components

## Voice Client (`app/`)

Handles Python-based interaction:

- microphone recording
- Whisper speech-to-text
- API communication
- text-to-speech playback (`pyttsx3`)

### Run

```bash
python app/main.py
```

---

## Web Interface (`web/`)

Browser-based conversational UI:

- text input
- microphone input
- persistent chat history
- browser speech synthesis
- interaction state feedback
- synchronized memory reset

### Run

```bash
cd web
python -m http.server 3000
```

### Open

```text
http://localhost:3000
```

---

## Browser Compatibility

Voice input uses the Web Speech API.

### Supported

- Chrome
- Edge

### Not Supported

- Firefox

---

## API Backend (`api/`)

Built with FastAPI.

### Responsibilities

- memory retrieval
- memory enrichment
- prompt construction
- reflection generation
- short-term conversation tracking
- communication with Ollama
- memory lifecycle management

### Run

```bash
uvicorn api.server:app --reload
```

---

## Agent Brain (`app/brain.py`)

The brain layer orchestrates:

- layered memory retrieval
- memory filtering
- prompt grounding
- context prioritization

It acts as the reasoning coordinator between memory and generation.

---

## LLM Service

Powered locally with Ollama.

### Current Model

- Llama 3

### Run

```bash
ollama run llama3
```

---

# Memory System

## Current Design

The memory system combines:

- Sentence Transformers embeddings
- FAISS vector similarity search
- LLM-based fact extraction
- reflection synthesis
- layered memory retrieval

### Embedding Model

```text
all-MiniLM-L6-v2
```

---

# Memory Types

The system now stores different categories of memory.

---

## 1. Conversation Memory

Raw conversational history.

### Example

```text
User: I own 2 dogs
```

### Used For

- short-term continuity
- conversational flow

---

## 2. Fact Memory

Durable structured information extracted from conversations.

### Example

```text
User owns 2 dogs
```

### Used For

- long-term recall
- personalization
- retrieval grounding

---

## 3. Reflection Memory

Higher-level insights inferred from accumulated facts.

### Example

```text
User is an animal lover
User values companionship
```

### Used For

- personality continuity
- behavioral grounding
- deeper contextual prompting

---

# Memory Pipeline

After each interaction:

```text
Conversation
↓
Fact Extraction
↓
Fact Storage
↓
Periodic Reflection Generation
↓
Reflection Storage
↓
Semantic Retrieval
↓
Prompt Construction
↓
LLM Response
```

---

# Reflection System (Unit 2.1)

The agent periodically synthesizes higher-level reflections from stored facts.

### Examples

- User values companionship
- User enjoys caring for animals
- User prioritizes playful activities

This moves the system beyond raw memory storage into primitive behavioral modeling.

---

# Layered Retrieval (Unit 2.2)

Memory retrieval now combines:

- recent conversation memories
- durable facts
- higher-level reflections

This significantly improves:

- conversational continuity
- personalization
- long-term consistency
- contextual grounding

---

# Memory Storage

Memories are persisted locally:

```text
data/memory.index
data/memory.json
```

The system survives API restarts.

---

# API Endpoints

## `POST /ask`

### Request

```json
{
  "query": "Tell me something about my pets"
}
```

### Response

```json
{
  "query": "...",
  "response": "...",
  "memory_used": [...]
}
```

---

## `POST /reset`

Clears:

- FAISS index
- stored memories
- conversation history

### Response

```json
{
  "status": "memory_cleared"
}
```

---

# Full Pipeline

```text
Voice/Text Input
↓
Speech Recognition (optional)
↓
Memory Retrieval
↓
Layered Context Assembly
↓
Prompt Construction
↓
LLM Generation
↓
Fact Extraction
↓
Reflection Generation
↓
Memory Storage
↓
TTS / UI Response
```

---

# Features

- fully local execution
- semantic vector memory
- layered memory architecture
- durable fact extraction
- reflection synthesis
- contextual prompt grounding
- modular brain layer
- browser + Python interfaces
- synchronized memory reset
- persistent local memory
- retrieval filtering
- FAISS semantic search
- Ollama local inference

---

# Current Limitations

- reflection quality depends heavily on the LLM
- reflections can still hallucinate weak personality traits
- no structured memory conflict resolution yet
- no streaming responses
- browser voice support limited to Chrome/Edge
- memory ranking heuristics are still simplistic
- no multi-user isolation yet

---

# Future Improvements

## Memory

- memory decay
- confidence scoring
- contradiction detection
- temporal memories
- episodic memory grouping
- hybrid symbolic + semantic retrieval

---

## Agent Intelligence

- planning layer
- tool usage
- goal tracking
- autonomous reflection scheduling
- reinforcement-based memory ranking

---

## Infrastructure

- Docker deployment
- Redis caching
- PostgreSQL / vector DB support
- Kubernetes orchestration
- streaming inference
- async processing

---

# Summary

This project has evolved from a simple conversational assistant into a layered memory AI architecture capable of:

- storing conversations
- extracting durable knowledge
- generating higher-level reflections
- retrieving contextual memories semantically
- grounding future responses using long-term context

The system is now approaching the foundations of a true persistent conversational agent with evolving memory and behavioral continuity.