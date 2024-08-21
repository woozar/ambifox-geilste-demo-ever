#!/bin/zsh

export OPENAI_API_KEY=""
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY=""

python3 create-report.py
