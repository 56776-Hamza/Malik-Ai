"""Command-line entry point for Malik-AI."""

from app.assistant import MalikAssistant, OllamaError
from app.config import settings


def main() -> None:
    """Run an interactive terminal chat session."""
    assistant = MalikAssistant()

    print("Malik-AI — local assistant")
    print(f"Model: {settings.ollama_model}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nMalik: Goodbye!")
            break

        if prompt.lower() in {"exit", "quit"}:
            print("Malik: Goodbye!")
            break
        if not prompt:
            continue

        try:
            print(f"Malik: {assistant.ask(prompt)}\n")
        except OllamaError as exc:
            print(f"Malik: {exc}\n")


if __name__ == "__main__":
    main()
