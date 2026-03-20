#!/bin/bash
PORT=${1:-8081}
uv run uvicorn bass.app:app --port "$PORT" --app-dir src --reload
