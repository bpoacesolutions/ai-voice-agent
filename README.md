# AI Voice Agent

## Overview

This project implements a modular AI voice agent capable of:

* understanding spoken input
* retrieving contextual memory
* generating responses using a language model
* replying with synthesized speech

The system supports both:

* a **Python-based voice client**
* a **browser-based voice interface (full input/output loop with chat UI)**

It is designed with a clean separation between interface, backend logic, and model execution.

---

## Architecture

```text id="2kq1yn"
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

```bash id="v7x2kc"
python app/main.py
```

---

### Web Interface (`web/`)

Browser-based voice assistant with a **chat-style interface**:

* text input
* microphone input (speech recognition)
* automatic API requests
* **persistent conversation display (chat UI)**
* text-to-speech playback (browser)

Run:

```bash id="zq5l9w"
cd web
python -m http.server 3000
```

Open:

```text id="y8p2af"
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

```bash id="o3rm9n"
uvicorn api.server:app
```

---

### Language Model

Powered by Ollama:

* Llama 3

Run locally:

```bash id="4xj7qe"
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

```json id="qk8m2r"
{
  "query": "What should I eat tonight?"
}
```

Response:

```json id="1j9v5c"
{
  "query": "...",
  "response": "...",
  "memory_used": [...]
}
```

---

## Full Pipeline

```text id="p7z1wr"
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
↓
Chat UI update (browser)
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

## Chat Interface

The web interface now includes a **chat-style conversation view**.

### Features

* messages are appended instead of replaced
* clear distinction between user and agent messages
* automatic scrolling
* supports multi-turn conversations

### Behavior

```text id="g5r8zp"
User message
↓
Displayed in chat
↓
API request
↓
Agent response
↓
Appended to chat
```

---

## Interaction Flow

```text id="k1b3yt"
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

```bash id="9c1vqx"
ollama run llama3
```

---

### 2. Start API

```bash id="0k2zrm"
uvicorn api.server:app
```

---

### 3A. Run Voice Client (Python)

```bash id="3f9pzn"
python app/main.py
```

---

### 3B. Run Web Interface

```bash id="8w2qjl"
cd web
python -m http.server 3000
```

Open:

```text id="6p4kdx"
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
* **chat-based conversation UI**

---

## Limitations

* browser voice input only works in Chrome/Edge (not Firefox)
* noticeable latency (especially TTS)
* no streaming responses
* in-memory storage (no persistence)
* chat history is not persisted (resets on refresh)
* voice quality depends on browser/OS

---

## Future Improvements

* persistent chat history (backend storage)
* streaming responses (reduce latency)
* real-time speech detection (VAD)
* improved memory (vector database)
* tool integration (weather, finance, etc.)
* deployment (cloud / containerization)

---

## Summary

This project demonstrates a complete full-stack AI system with:

* a voice interface (Python)
* a browser-based voice assistant (input + output + chat UI)
* a backend API service
* a local language model

It serves as a foundation for building real-world conversational AI applications.
