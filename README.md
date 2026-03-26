# Bass — AI Banking Assistant

An LLM-powered virtual banking assistant built with Python, FastAPI, and modern AI tooling.

## What is this?

A conversational AI assistant for banking customers that:
- Answers questions about bank products, policies, and FAQs (RAG)
- Handles multi-step workflows: intent classification, retrieval, response, escalation (Agents)
- Uses tools to look up account info and transaction history (Tool Use / MCP)
- Detects when to escalate to a human agent
- Tracks conversation quality, hallucination rate, and cost

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Package manager | uv |
| Web framework | FastAPI |
| Data models | Pydantic v2 |
| LLM orchestration | LangChain / LangGraph |
| Vector database | pgvector (PostgreSQL) |
| Evaluation | DeepEval, RAGAS |
| Observability | LangSmith / Langfuse |
| LLM provider | Anthropic Claude / AWS Bedrock |
| Deployment | Docker, AWS ECS |

## Project Structure

```
src/bass/
├── app.py                 # FastAPI app setup
├── models/
│   └── conversation.py    # Pydantic models (Message, Conversation)
├── storage/
│   └── conversations.py   # Data access layer
├── services/
│   ├── conversation.py    # Business logic
│   └── llm_service.py     # LLM integration (echo mode for now)
└── routes/
    └── conversations.py   # API endpoints

static/                    # Frontend (Alpine.js + Tailwind)
tests/                     # pytest test suite
```

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python package manager

### Setup

```bash
uv install
```

### Run the server

```bash
./start.sh          # starts on port 8081
./start.sh 3000     # or specify a port
```

Then open `http://localhost:8081` in your browser.

### Development

```bash
uv run ruff check .      # lint
uv run ruff format .     # format
uv run mypy src/         # type check
uv run pytest            # run tests
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/conversations` | Create a new conversation |
| `GET` | `/conversations` | List all conversations |
| `GET` | `/conversations/{id}` | Get conversation with messages |
| `DELETE` | `/conversations/{id}` | Delete a conversation |
| `POST` | `/conversations/{id}/messages` | Send a message, get response |

## Current Status

Phase 1 (Foundation) — echo chat with REST API and web UI. LLM integration coming next.
