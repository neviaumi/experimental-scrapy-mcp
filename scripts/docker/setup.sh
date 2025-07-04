#!/bin/bash
set -ex
apk add gcc musl-dev linux-headers

uv sync --no-dev
