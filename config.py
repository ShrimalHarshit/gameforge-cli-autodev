import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "model": "codellama:7b",
    "endpoint": "http://localhost:11434/api/generate",
    "history_limit": 20,
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 1024,
    "stream": True,
    "show_thinking": False,
    "auto_trim": True,
    "config_file": str(Path.home() / ".gameforge" / "config.json")
}

class Config:
    """Configuration manager for GameForge CLI."""
    
    def __init__(self, config_path: Optional[str] = None) -> None:
        self._config_path = Path(config_path) if config_path else Path(DEFAULT_CONFIG["config_file"])
        self._data: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self) -> None:
        """Load configuration from file, creating defaults if missing."""
        try:
            if self._config_path.exists():
                with self._config_path.open("r", encoding="utf-8") as f:
                    file_data = json.load(f)
                # Merge with defaults to ensure all keys exist
                self._data.update(file_data)
            else:
                self.save()  # Create default config file
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Could not load config from {self._config_path}: {e}")
            print("Using default configuration.")
            self._data = DEFAULT_CONFIG.copy()
    
    def save(self) -> None:
        """Save current configuration to file."""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            with self._config_path.open("w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, sort_keys=True)
        except OSError as e:
            print(f"Error: Could not save config to {self._config_path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and persist to file."""
        self._data[key] = value
        self.save()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self._data.update(updates)
        self.save()
    
    def as_dict(self) -> Dict[str, Any]:
        """Return a copy of the configuration as a dictionary."""
        return self._data.copy()
    
    # Convenience properties for commonly accessed settings
    @property
    def model(self) -> str:
        return self.get("model", DEFAULT_CONFIG["model"])
    
    @model.setter
    def model(self, value: str) -> None:
        self.set("model", value)
    
    @property
    def endpoint(self) -> str:
        return self.get("endpoint", DEFAULT_CONFIG["endpoint"])
    
    @endpoint.setter
    def endpoint(self, value: str) -> None:
        self.set("endpoint", value)
    
    @property
    def history_limit(self) -> int:
        return self.get("history_limit", DEFAULT_CONFIG["history_limit"])
    
    @history_limit.setter
    def history_limit(self, value: int) -> None:
        self.set("history_limit", value)
    
    @property
    def temperature(self) -> float:
        return self.get("temperature", DEFAULT_CONFIG["temperature"])
    
    @temperature.setter
    def temperature(self, value: float) -> None:
        self.set("temperature", value)
    
    @property
    def top_p(self) -> float:
        return self.get("top_p", DEFAULT_CONFIG["top_p"])
    
    @top_p.setter
    def top_p(self, value: float) -> None:
        self.set("top_p", value)
    
    @property
    def max_tokens(self) -> int:
        return self.get("max_tokens", DEFAULT_CONFIG["max_tokens"])
    
    @max_tokens.setter
    def max_tokens(self, value: int) -> None:
        self.set("max_tokens", value)
    
    @property
    def stream(self) -> bool:
        return self.get("stream", DEFAULT_CONFIG["stream"])
    
    @stream.setter
    def stream(self, value: bool) -> None:
        self.set("stream", value)
    
    @property
    def show_thinking(self) -> bool:
        return self.get("show_thinking", DEFAULT_CONFIG["show_thinking"])
    
    @show_thinking.setter
    def show_thinking(self, value: bool) -> None:
        self.set("show_thinking", value)
    
    @property
    def auto_trim(self) -> bool:
        return self.get("auto_trim", DEFAULT_CONFIG["auto_trim"])
    
    @auto_trim.setter
    def auto_trim(self, value: bool) -> None:
        self.set("auto_trim", value)