#!/bin/bash

set -ex
uv sync
uv pip install --editable ./crawlers
uv pip install --editable ./