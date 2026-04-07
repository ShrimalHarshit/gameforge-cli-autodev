"""
history_manager.py
Manages conversation history for GameForge CLI with automatic context window trimming.
"""

import json
import os
from pathlib import Path


class HistoryManager:
    """Manages session-based conversation history with automatic context trimming."""

    def __init__(self, max_tokens: int = 8192, history_file: str = "gameforge_history.json") -> None:
        self.max_tokens = max_tokens
        self.history_file = history_file
        self.messages: list[dict[str, str]] = []
        self.load()

    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the conversation history and trim if necessary."""
        self.messages.append({"role": role, "content": content})
        self.trim_history()

    def get_history(self) -> list[dict[str, str]]:
        """Return a copy of the current conversation history."""
        return self.messages.copy()

    def clear_history(self) -> None:
        """Clear all conversation history and persist the change."""
        self.messages.clear()
        self.save()

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count using a simple character-based heuristic."""
        return max(1, len(text) // 4)

    def trim_history(self) -> None:
        """Remove oldest messages until the estimated token count fits within max_tokens."""
        total_tokens = sum(self._estimate_tokens(m["content"]) for m in self.messages)
        
        while total_tokens > self.max_tokens and len(self.messages) > 1:
            removed_idx = -1
            for i, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    removed_idx = i
                    break
            
            if removed_idx == -1:
                break
                
            removed = self.messages.pop(removed_idx)
            total_tokens -= self._estimate_tokens(removed["content"])

    def save(self) -> None:
        """Persist conversation history to disk."""
        try:
            Path(self.history_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Warning: Could not save history to {self.history_file}: {e}")

    def load(self) -> None:
        """Load conversation history from disk if it exists."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, list):
                        self.messages = loaded
                    else:
                        self.messages = []
            except (OSError, json.JSONDecodeError) as e:
                print(f"Warning: Could not load history from {self.history_file}: {e}")
                self.messages = []