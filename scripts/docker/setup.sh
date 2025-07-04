#!/bin/bash
set -ex
apk add gcc musl-dev linux-headers \
python3~=3.12 python3-dev~=3.12

uv sync --no-dev --locked
