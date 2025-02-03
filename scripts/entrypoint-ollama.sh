#!/bin/sh

ollama serve &

if ! ollama list | grep -q "llama3"; then
    echo "Downloading llama3 model..."
    ollama pull llama3
fi

if ! ollama list | grep -q "mistral"; then
    echo "Downloading mistral model..."
    ollama pull mistral
fi

if ! ollama list | grep -q "gemma"; then
    echo "Downloading gemma model..."
    ollama pull gemma
fi

wait
