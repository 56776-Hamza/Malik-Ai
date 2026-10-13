# Malik-AI Starter Architecture

## Purpose

This starter keeps inference local by sending chat requests to the Ollama service on the developer's machine. It does not require a cloud AI provider or cloud API key.

## Request flow

1. The command-line entry point in `app/main.py` reads a prompt.
2. `app/assistant.py` creates an Ollama `/api/chat` request.
3. Ollama runs the selected local model and returns a response.
4. Malik prints the response in the terminal.

## Modules

- `app/config.py`: loads model, endpoint, and timeout settings from environment variables.
- `app/assistant.py`: handles the HTTP request and turns common connection/HTTP failures into readable errors.
- `app/main.py`: interactive terminal loop.
- `tests/test_assistant.py`: mocked unit tests that do not need Ollama.

## Security notes

- Keep the real `.env` file untracked; only commit `.env.example`.
- Do not add passwords, API keys, access tokens, or private data to source control.
- The default endpoint is localhost. If you change it to a network endpoint, make sure the destination is trusted.
- The model receives the prompts you type into the assistant. Avoid sending sensitive information unless you understand your local model/runtime setup.

## Planned extensions

Conversation history, streaming output, voice I/O, a web interface, and optional tools can be added as separate features after the foundation is verified.
