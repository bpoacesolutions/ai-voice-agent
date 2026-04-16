# AI Voice Agent

## Overview

This project implements a modular AI voice agent capable of:

* understanding spoken input
* retrieving contextual memory
* generating responses using a language model
* replying with synthesized speech

The system is designed with a clean separation between interface, backend logic, and model execution.

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

Handles user interaction via Python:

* audio recording (microphone)
* speech-to-text transcription (Whisper)
* API communication
* text-to-speech playback

Entry point:

```bash
python app/main.py
```

---

### Web Interface (`web/`)

Lightweight browser-based UI:

* text input
* API communication
* response display

Run:

```text
open web/index.html
```

---

### API Backend (`api/`)

Built with FastAPI

Responsibilities:

* semantic memory retrieval (embeddings)
* prompt construction
* conversation history management
* communication with the LLM

Run with:

```bash
uvicorn api.server:app
```

---

### Language Model

Powered by Ollama using:

* Llama 3

Run locally:

```bash
ollama run llama3
```

---

### Memory System

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
Speech input (Python client)
        OR
Text input (Web UI)
↓
API request (/ask)
↓
Memory retrieval
↓
Prompt construction
↓
LLM response
↓
Text-to-speech (Python client)
        OR
Text display (Web UI)
```

---

## Running the System

### 1. Start LLM

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

### 3B. Run Web Interface (Browser)

```text
open web/index.html
```

---

## CORS Configuration

CORS is enabled in the API to allow communication between the browser and backend during local development.

---

## Features

* fully local execution
* modular architecture (client / backend / model)
* semantic memory retrieval
* continuous interaction loop (voice or text)
* API-first design (ready for web or mobile integration)
* dual interface (CLI voice + browser UI)

---

## Limitations

* fixed recording duration (voice client)
* noticeable latency (especially TTS)
* no streaming responses
* in-memory storage (no persistence)
* web UI does not yet preserve conversation history

---

## Future Improvements

* conversation timeline in web UI
* browser-based voice input (microphone)
* audio playback in browser
* real-time speech detection (VAD)
* streaming responses
* faster / higher quality TTS
* persistent memory (database)
* deployment (cloud / containerization)

---

## Summary

This project demonstrates a complete full-stack AI system with:

* a voice interface (Python)
* a browser interface (Web)
* a backend API service
* a local language model

and a clean separation of concerns suitable for real-world applications.
