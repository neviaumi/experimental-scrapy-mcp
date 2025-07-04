#!/bin/bash
set -ex
MODE=${1:---dev}

if [ "$MODE" == "--dev" ]; then
  uv run fastapi dev --port 8080 src/app/main.py
elif [ "$MODE" == "--prod" ]; then
  uv run fastapi run --port 8081 src/app/main.py
else
    echo "Invalid argument: $MODE"
    exit 1
fi

