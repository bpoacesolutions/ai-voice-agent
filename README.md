# AI Voice Agent

## Overview

This project implements a modular AI agent capable of:

* understanding user input
* retrieving contextual memory
* generating responses using a language model
* exposing functionality via an API

---

## API Layer

The agent is exposed through a REST API built with:

* FastAPI

### Endpoint

```text
POST /ask
```

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

## Running the API

```bash
uvicorn api.server:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Architecture

```text
User input
↓
Memory retrieval (embeddings)
↓
Prompt construction
↓
LLM (Ollama)
↓
Response
```

---

## Next Steps

* integrate voice input/output
* connect frontend interface
* optimize latency
