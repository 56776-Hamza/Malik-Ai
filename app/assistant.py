"""Minimal client for the local Ollama chat API."""

from typing import Any

import requests

from app.config import settings


class OllamaError(RuntimeError):
    """Raised when Ollama cannot provide a response."""


class MalikAssistant:
    """Send prompts to a locally running Ollama model."""

    def __init__(
        self,
        base_url: str = settings.ollama_base_url,
        model: str = settings.ollama_model,
        timeout_seconds: int = settings.ollama_timeout_seconds,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def ask(self, prompt: str) -> str:
        """Return the model's response for a single user prompt."""
        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            raise ValueError("Prompt cannot be empty.")

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Malik, a helpful personal AI assistant. "
                        "Be clear, practical, and honest about uncertainty."
                    ),
                },
                {"role": "user", "content": cleaned_prompt},
            ],
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise OllamaError(
                f"Could not connect to Ollama at {self.base_url}. "
                "Make sure Ollama is installed and running."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise OllamaError(
                "Ollama took too long to respond. Increase "
                "OLLAMA_TIMEOUT_SECONDS or try a smaller model."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "unknown"
            detail = ""
            if exc.response is not None:
                try:
                    detail = exc.response.json().get("error", "")
                except ValueError:
                    detail = exc.response.text[:300]
            message = f"Ollama returned HTTP {status}."
            if detail:
                message += f" Details: {detail}"
            if status == 404:
                message += f" Check that model '{self.model}' is downloaded (ollama pull {self.model})."
            raise OllamaError(message) from exc
        except requests.exceptions.RequestException as exc:
            raise OllamaError(f"Request to Ollama failed: {exc}") from exc

        try:
            data = response.json()
            answer = data["message"]["content"].strip()
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            raise OllamaError("Ollama returned an unexpected response format.") from exc

        if not answer:
            raise OllamaError("Ollama returned an empty response.")
        return answer
