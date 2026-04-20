# AI Voice Agent

## Overview

This project implements a modular AI voice agent capable of:

* understanding spoken input
* retrieving contextual memory
* generating responses using a language model
* replying with synthesized speech

The system supports both:

* a **Python-based voice client**
* a **browser-based voice interface (full input/output loop)**

It is designed with a clean separation between interface, backend logic, and model execution.

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

Browser-based voice assistant with full interaction loop:

* text input
* microphone input (speech recognition)
* automatic API requests
* response display
* text-to-speech playback (browser)

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

### API Backend (`api/`)

Built with FastAPI

Responsibilities:

* semantic memory retrieval (embeddings)
* prompt construction
* conversation history management
* communication with the LLM

Run:

```bash
uvicorn api.server:app
```

---

### Language Model

Powered by Ollama:

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
LLM response
↓
Text-to-speech (Python or Browser)
```

---

## Browser Voice Interaction

The web interface uses native browser APIs to handle voice input and output.

### Input (Speech Recognition)

* Web Speech API
* real-time transcription
* automatic request triggering

### Output (Speech Synthesis)

* browser-native text-to-speech
* automatic playback of responses

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

A status indicator provides real-time feedback to the user.

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

---

## Limitations

* browser voice input only works in Chrome/Edge (not Firefox)
* noticeable latency (especially TTS)
* no streaming responses
* in-memory storage (no persistence)
* web UI does not preserve conversation history yet
* voice quality depends on browser/OS

---

## Future Improvements

* conversation timeline (chat-style UI)
* streaming responses (faster perceived latency)
* real-time speech detection (VAD)
* improved memory (vector database)
* tool integration (weather, finance, etc.)
* persistent storage (database)
* deployment (cloud / containerization)

---

## Summary

This project demonstrates a complete full-stack AI system with:

* a voice interface (Python)
* a browser-based voice assistant (input + output)
* a backend API service
* a local language model

It serves as a foundation for building real-world conversational AI applications.
