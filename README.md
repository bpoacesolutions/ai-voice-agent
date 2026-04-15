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
Voice Client (app/)
↓
API Backend (api/)
↓
LLM Service (Ollama)
```

---

## Components

### Voice Client (`app/`)

Handles user interaction:

* audio recording (microphone)
* speech-to-text transcription
* API communication
* text-to-speech playback

Entry point:

```bash
python app/main.py
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
Speech input
↓
Speech-to-text (Whisper)
↓
API request (/ask)
↓
Memory retrieval
↓
Prompt construction
↓
LLM response
↓
Text-to-speech
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

### 3. Start Voice Client

```bash
python app/main.py
```

---

## Features

* fully local execution
* modular architecture (client / backend / model)
* semantic memory retrieval
* continuous voice interaction loop
* API-first design (ready for web or mobile integration)

---

## Limitations

* fixed recording duration
* noticeable latency (especially TTS)
* no streaming responses
* in-memory storage (no persistence)

---

## Future Improvements

* browser-based interface
* real-time speech detection (VAD)
* streaming responses
* faster / higher quality TTS
* persistent memory (database)
* deployment (cloud / containerization)

---

## Summary

This project demonstrates a complete AI system with:

* a voice interface
* a backend service
* a local language model

and a clean separation of concerns suitable for real-world applications.
