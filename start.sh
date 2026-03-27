#!/bin/bash
PORT=${1:-8081}

echo "Running mypy type checking..."
uv run mypy src

if [ $? -ne 0 ]; then
    echo "❌ Mypy validation failed! Fix type errors before running the app."
    exit 1
fi

echo "✅ Mypy validation passed!"
uv run uvicorn bass.app:app --port "$PORT" --app-dir src --reload
