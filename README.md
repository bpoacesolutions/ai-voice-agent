# AI Voice Agent

## Overview

This project implements a modular AI voice agent capable of:

* understanding spoken input
* retrieving contextual memory
* generating responses using a language model
* replying with synthesized speech

The system supports both:

* a **Python-based voice client**
* a **browser-based voice assistant (full input/output loop with chat UI)**

It is designed with a clean separation between interface, backend logic, and model execution, following a **service-oriented architecture**.

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
* text-to-speech playback

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

The voice features rely on the **Web Speech API**, which is **not supported in all browsers**.

### Supported

* Chrome ✅
* Edge ✅

### Not Supported

* Firefox ❌

If the microphone button appears unresponsive, ensure you are using **Chrome** and that microphone permissions are enabled.

---

### API Backend (`api/`)

Built with FastAPI

Responsibilities:

* semantic memory retrieval (embeddings)
* prompt construction
* conversation history management
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

## Important: LLM Service Dependency

The API depends on a locally running LLM service.

If Ollama is not running, requests to `/ask` will fail with connection errors such as:

```text
ConnectionRefusedError: localhost:11434
```

### Resolution

Start the LLM before using the system:

```bash
ollama run llama3
```

---

## Memory System

Uses:

* sentence-transformers
* scikit-learn

Features:

* semantic similarity search
* contextual memory retrieval
* short-term conversation history

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
Memory retrieval
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

## Browser Voice Interaction

The web interface uses native browser APIs.

### Input (Speech Recognition)

* Web Speech API
* real-time transcription
* automatic request triggering
* error handling and fallback feedback

### Output (Speech Synthesis)

* browser-native text-to-speech
* dynamic voice selection (when available)
* playback status tracking

---

## Chat Interface

The web interface includes a **chat-style conversation view**.

### Features

* messages are appended (not replaced)
* clear distinction between user and agent
* automatic scrolling
* multi-turn conversations
* persisted locally (via localStorage)

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

A status indicator provides real-time feedback during interaction.

---

## Running the System

### 1. Start LLM Service

```bash
ollama run llama3
```

---

### 2. Start API

```bash
uvicorn api.server:app
```

---

### 3A. Run Voice Client (Python)

```bash
python app/main.py
```

---

### 3B. Run Web Interface

```bash
cd web
python -m http.server 3000
```

Open:

```text
http://localhost:3000
```

---

## CORS Configuration

CORS is enabled in the API to allow browser-to-backend communication during local development.

---

## Features

* fully local execution
* modular architecture (client / backend / model)
* semantic memory retrieval
* continuous interaction loop (voice + text)
* API-first design
* dual interface:

  * Python voice client
  * browser voice assistant (input + output)
* real-time interaction feedback (status indicator)
* chat-based UI with persistence
* decoupled LLM service (production-style architecture)
* improved frontend robustness (error handling, browser checks)

---

## Limitations

* browser voice input only works in Chrome/Edge
* noticeable latency (especially TTS)
* no streaming responses
* in-memory backend storage (no persistence)
* chat history is only stored locally (browser)
* voice quality depends on browser/OS
* requires local LLM service to be running

---

## Future Improvements

* vector memory (FAISS) for semantic long-term memory
* persistent backend storage (database)
* streaming responses (reduce latency)
* real-time speech detection (VAD)
* tool integration (weather, finance, etc.)
* deployment (cloud / containerization)
* LLM health checks / fallback mechanisms

---

## Summary

This project demonstrates a complete full-stack AI system with:

* a voice interface (Python)
* a browser-based voice assistant (input + output + chat UI)
* a backend API service
* a local language model service

It reflects real-world AI architecture patterns, including **service separation, dependency management, and conversational pipelines**, and serves as a strong foundation for building production-grade AI agents.
