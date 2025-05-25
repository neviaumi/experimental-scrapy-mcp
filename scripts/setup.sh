#!/bin/bash

set -ex
uv sync
uv pip install --editable ./crawlers