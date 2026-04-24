# AI Voice Agent

## Overview

This project implements a modular AI voice agent capable of:

* understanding spoken or typed input
* retrieving contextual memory using vector search (FAISS)
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

* Chrome ✅
* Edge ✅

### Not Supported

* Firefox ❌

If the microphone button appears unresponsive, use **Chrome** and allow microphone access.

---

### API Backend (`api/`)

Built with FastAPI.

Responsibilities:

* semantic memory retrieval (FAISS vector search)
* prompt construction
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

Capabilities:

* semantic retrieval of past interactions
* contextual grounding for responses

### Important Limitation

The system currently uses **only semantic memory**, which means:

* works well for similar phrasing
* may fail for **structured recall** (e.g. “how many pets do I have?”)

This highlights the need for:

* structured user memory (profile layer)
* improved retrieval strategies

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
Prompt construction
↓
LLM request (Ollama)
↓
LLM response
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
* vector memory is not sufficient for structured facts
* chat history only stored locally (browser)
* requires local LLM service

---

## Future Improvements

* structured user memory (profile layer)
* persistent memory storage (disk or database)
* hybrid retrieval (semantic + structured)
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
* backend API orchestration
* local LLM integration

It serves as a strong foundation for building **production-grade conversational AI agents**, and highlights key challenges such as **memory design and retrieval strategy**.
