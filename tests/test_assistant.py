"""Unit tests for MalikAssistant that do not require a running Ollama server."""

import unittest
from unittest.mock import Mock, patch

import requests

from app.assistant import MalikAssistant, OllamaError


class MalikAssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assistant = MalikAssistant(
            base_url="http://localhost:11434/",
            model="test-model",
            timeout_seconds=5,
        )

    def test_ask_sends_prompt_and_returns_content(self) -> None:
        response = Mock()
        response.json.return_value = {"message": {"content": "Hello from Malik!"}}
        response.raise_for_status.return_value = None

        with patch("app.assistant.requests.post", return_value=response) as post:
            answer = self.assistant.ask("Hello")

        self.assertEqual(answer, "Hello from Malik!")
        post.assert_called_once_with(
            "http://localhost:11434/api/chat",
            json={
                "model": "test-model",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Malik, a helpful personal AI assistant. "
                            "Be clear, practical, and honest about uncertainty."
                        ),
                    },
                    {"role": "user", "content": "Hello"},
                ],
                "stream": False,
            },
            timeout=5,
        )

    def test_empty_prompt_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.assistant.ask("   ")

    def test_connection_error_has_helpful_message(self) -> None:
        with patch(
            "app.assistant.requests.post",
            side_effect=requests.exceptions.ConnectionError("offline"),
        ):
            with self.assertRaisesRegex(OllamaError, "Make sure Ollama is installed and running"):
                self.assistant.ask("Hello")

    def test_unexpected_response_is_reported(self) -> None:
        response = Mock()
        response.json.return_value = {"unexpected": "shape"}
        response.raise_for_status.return_value = None

        with patch("app.assistant.requests.post", return_value=response):
            with self.assertRaisesRegex(OllamaError, "unexpected response format"):
                self.assistant.ask("Hello")


if __name__ == "__main__":
    unittest.main()
