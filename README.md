# AI Voice Agent

## Overview

This project implements a modular AI voice agent capable of:

* understanding spoken or typed input
* retrieving contextual memory using vector search (FAISS)
* extracting and storing structured knowledge from conversations
* generating responses using a local language model
* replying with synthesized speech

The system supports both:

* a **Python-based voice client**
* a **browser-based voice assistant (full input/output loop with chat UI)**

It follows a **service-oriented architecture**, separating interface, backend logic, and model execution.

---

## Architecture

```text
Voice Client (app/)        OR        Web Interface (web/)
            ↓
        API Backend (api/)
            ↓
     LLM Service (Ollama)
```

---

## Components

### Voice Client (`app/`)

Handles interaction via Python:

* audio recording (microphone)
* speech-to-text transcription (Whisper)
* API communication
* text-to-speech playback (pyttsx3 with multiprocessing)

Run:

```bash
python app/main.py
```

---

### Web Interface (`web/`)

Browser-based voice assistant with a **chat-style interface**:

* text input
* microphone input (speech recognition)
* automatic API requests
* persistent conversation display (localStorage)
* browser-based text-to-speech playback
* real-time interaction status (Listening / Thinking / Speaking)

Run:

```bash
cd web
python -m http.server 3000
```

Open:

```text
http://localhost:3000
```

---

## Browser Compatibility (Important)

Voice input relies on the **Web Speech API**.

### Supported

* Chrome
* Edge

### Not Supported

* Firefox

If the microphone button appears unresponsive, use **Chrome** and allow microphone access.

---

### API Backend (`api/`)

Built with FastAPI.

Responsibilities:

* semantic memory retrieval (FAISS vector search)
* LLM-based memory enrichment (fact extraction)
* memory filtering (distance-based relevance)
* prompt construction with guided reasoning
* short-term conversation tracking
* communication with the LLM service

Run:

```bash
uvicorn api.server:app
```

---

### Language Model Service

Powered by Ollama:

* Llama 3

Run locally:

```bash
ollama run llama3
```

---

## Important: LLM Dependency

The API depends on a locally running LLM.

If Ollama is not running, requests will fail with:

```text
ConnectionRefusedError: localhost:11434
```

Start it before using the system:

```bash
ollama run llama3
```

---

## Memory System

### Current Design

Uses:

* sentence-transformers (`all-MiniLM-L6-v2`)
* FAISS (vector similarity search)
* LLM-based memory summarization
* distance-based filtering for retrieval quality

---

### How It Works

After each interaction:

1. Raw conversation is stored
2. The LLM extracts **durable user facts**
3. Facts are stored as independent memory entries
4. Future queries retrieve relevant memories via FAISS
5. Low-quality matches are filtered using similarity distance

---

### Example

Input:

```text
User: I have 3 cats and 1 dog
```

Stored as:

```text
User: I have 3 cats and 1 dog
User owns 3 cats
User owns 1 dog
```

---

### Retrieval Improvement (Unit 1.3)

The system now uses **filtered semantic retrieval**:

* retrieves top-k memories
* removes low-relevance results (distance threshold)
* falls back to best matches if filtering is too strict

This significantly improves:

* recall accuracy
* consistency of answers
* resistance to noisy memory

---

## API Endpoint

### POST `/ask`

Request:

```json
{
  "query": "What should I eat tonight?"
}
```

Response:

```json
{
  "query": "...",
  "response": "...",
  "memory_used": [...]
}
```

---

## Full Pipeline

```text
Voice input (Python or Browser)
        OR
Text input (Browser)
↓
Speech Recognition (if applicable)
↓
API request (/ask)
↓
Vector memory retrieval (FAISS)
↓
Memory filtering (distance threshold)
↓
Prompt construction (guided reasoning)
↓
LLM request (Ollama)
↓
LLM response
↓
Memory enrichment (fact extraction)
↓
Text-to-speech (Python or Browser)
↓
Chat UI update (browser)
```

---

## Chat Interface

The web interface includes a **chat-style conversation view**.

Features:

* messages appended (not replaced)
* clear user/agent separation
* automatic scrolling
* multi-turn conversations
* persisted locally via localStorage

---

## Interaction Flow

```text
Idle
→ 🎤 Listening...
→ Processing...
→ Thinking...
→ 🔊 Speaking...
→ Idle
```

---

## Features

* fully local execution

* modular architecture (client / backend / model)

* semantic memory with FAISS

* LLM-powered memory enrichment (structured facts)

* **improved retrieval with filtering (Unit 1.3)**

* continuous interaction loop (voice + text)

* API-first design

* dual interface:

  * Python voice client
  * browser voice assistant

* real-time interaction feedback (status indicator)

* chat-based UI with persistence

* decoupled LLM service (production-style architecture)

---

## Limitations

* browser voice input only works in Chrome/Edge
* noticeable latency (LLM + TTS)
* no streaming responses
* backend memory is not persisted (resets on restart)
* no structured reasoning layer (prompt-based only)
* aggregation logic (e.g. “total pets”) is still imperfect
* chat history only stored locally (browser)
* requires local LLM service

---

## Future Improvements

* memory deduplication and ranking (Unit 1.4)
* memory reset endpoint (conversation lifecycle control)
* structured user profile layer (hybrid memory)
* persistent memory storage (disk or database)
* hybrid retrieval (semantic + keyword / structured)
* streaming responses
* real-time speech detection (VAD)
* tool integration (APIs, external data)
* deployment (Docker / cloud)
* LLM health checks & fallback

---

## Summary

This project demonstrates a full-stack AI system with:

* voice interaction (Python + browser)
* semantic memory (FAISS)
* LLM-driven knowledge extraction
* improved retrieval with filtering and prompt guidance
* backend API orchestration
* local LLM integration

It now moves beyond simple conversation history and introduces **knowledge-aware memory with retrieval control**, forming the foundation of a real **RAG-style AI agent**.
