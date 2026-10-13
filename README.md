# Malik-AI

Malik-AI is a personal AI assistant starter project built with Python and [Ollama](https://ollama.com/) for local language-model inference.

This repository currently contains the project foundation: configuration, a small CLI chat loop, an Ollama client, tests, and setup documentation.

## Features

- Run models locally through Ollama.
- Configure the Ollama URL and model name with environment variables.
- Keep secrets and local environment files out of version control.
- Simple, beginner-friendly Python structure.
- Unit tests for assistant response handling.

## Requirements

- Python 3.10+
- [Ollama installed and running](https://ollama.com/download)
- A model downloaded locally, for example `llama3.2`

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/56776-Hamza/Malik-Ai.git
cd Malik-Ai
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start Ollama and download a model

Make sure the Ollama application/service is running, then run:

```bash
ollama pull llama3.2
```

### 5. Configure Malik

Copy `.env.example` to `.env` and adjust values if needed.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Default configuration uses `http://localhost:11434` and model `llama3.2`. The app reads `.env` values using python-dotenv.

### 6. Run the assistant

```bash
python -m app.main
```

Type `exit` or `quit` to end the session.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Base URL for the local Ollama API |
| `OLLAMA_MODEL` | `llama3.2` | Local model tag to use |
| `OLLAMA_TIMEOUT_SECONDS` | `120` | HTTP timeout for model responses |

No cloud API key is required for this local setup. Never commit your real `.env` file, credentials, or tokens.

## Project structure

```text
Malik-AI/
├── app/
│   ├── __init__.py
│   ├── assistant.py
│   ├── config.py
│   └── main.py
├── docs/
│   └── architecture.md
├── tests/
│   └── test_assistant.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

Tests use a mocked HTTP response and do not require Ollama to be running.

## Troubleshooting

- **Connection refused:** Start Ollama and confirm it is listening at `OLLAMA_BASE_URL`.
- **Model not found:** Run `ollama pull llama3.2` or set `OLLAMA_MODEL` to a model you already downloaded.
- **Slow responses:** Increase `OLLAMA_TIMEOUT_SECONDS` in your local `.env` file.

## Roadmap

- [x] Python project foundation
- [x] Local Ollama chat client
- [x] Environment-based configuration
- [x] Starter tests and documentation
- [ ] Conversation memory
- [ ] Voice input and spoken responses
- [ ] Optional web interface and tool integrations

## License

No license has been added yet. Until one is chosen, the repository's default copyright rules apply.
