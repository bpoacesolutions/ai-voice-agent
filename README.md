# AI Voice Agent

## Overview

This project implements a modular AI voice agent capable of:

* understanding spoken input
* retrieving contextual memory
* generating responses using a language model
* replying with synthesized speech

The system is designed with a clean separation between interface, backend logic, and model execution, and supports both **Python-based voice interaction** and **browser-based interaction**.

---

## Architecture

```text id="3z9t5h"
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

```bash id="f6n9xu"
python app/main.py
```

---

### Web Interface (`web/`)

Lightweight browser-based UI with voice capabilities:

* text input
* microphone input (speech recognition)
* automatic API communication
* response display

Run:

```bash id="a7o2re"
cd web
python -m http.server 3000
```

Then open:

```text id="z2y5xv"
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

Run with:

```bash id="ybrqk1"
uvicorn api.server:app
```

---

### Language Model

Powered by Ollama using:

* Llama 3

Run locally:

```bash id="9k5q5y"
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

```json id="m6o0rn"
{
  "query": "What should I eat tonight?"
}
```

Response:

```json id="p2t9nz"
{
  "query": "...",
  "response": "...",
  "memory_used": [...]
}
```

---

## Full Pipeline

```text id="b7y9tw"
Speech input (Python client)
        OR
Speech/Text input (Web UI)
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

```bash id="g8o3dl"
ollama run llama3
```

---

### 2. Start API

```bash id="j9m2pf"
uvicorn api.server:app
```

---

### 3A. Run Voice Client (Python)

```bash id="v8q1ye"
python app/main.py
```

---

### 3B. Run Web Interface (Browser)

```bash id="w3n1fa"
cd web
python -m http.server 3000
```

Then open:

```text id="x1c8dy"
http://localhost:3000
```

---

## Browser Voice Interaction

The web interface supports voice input using the browser’s Web Speech API.

### Features

* microphone-based input
* real-time speech transcription
* automatic request triggering
* seamless API integration

### How It Works

```text id="y6k4zq"
User clicks microphone
↓
Browser captures audio
↓
Speech Recognition (Web Speech API)
↓
Transcribed text inserted into input
↓
Automatic API request (/ask)
↓
LLM response displayed
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
* dual interface:

  * Python voice client
  * browser-based UI with speech input

---

## Limitations

* fixed recording duration (Python client)
* noticeable latency (especially TTS)
* no streaming responses
* in-memory storage (no persistence)
* web UI does not preserve conversation history yet
* no voice output in browser yet

---

## Future Improvements

* conversation timeline in web UI
* browser-based text-to-speech (agent voice)
* real-time speech detection (VAD)
* streaming responses
* faster / higher quality TTS
* persistent memory (database)
* deployment (cloud / containerization)

---

## Summary

This project demonstrates a complete full-stack AI system with:

* a voice interface (Python)
* a browser interface with speech input
* a backend API service
* a local language model

and a clean separation of concerns aligned with real-world AI application architecture.
