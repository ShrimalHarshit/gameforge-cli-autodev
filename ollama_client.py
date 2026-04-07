import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List
from config import Config, load

class OllamaClient:
    """
    Client for interacting with a local Ollama instance.
    Uses only Python standard library for HTTP requests.
    """

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Ollama client.

        Args:
            base_url: Base URL of the Ollama API (e.g., "http://localhost:11434").
                      If None, reads from config.
            model: Default model to use for generation.
                   If None, reads from config.
        """
        cfg = load()
        self.base_url = base_url if base_url is not None else cfg.get("ollama_host", "http://localhost:11434")
        self.model = model if model is not None else cfg.get("ollama_model", "llama3")
        # Ensure no trailing slash
        self.base_url = self.base_url.rstrip("/")

    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper to make a POST request to the Ollama API.

        Args:
            endpoint: API endpoint (e.g., "/api/generate").
            payload: JSON-serializable dict to send as request body.

        Returns:
            Parsed JSON response as a dict.

        Raises:
            RuntimeError: If the request fails or returns an error status.
        """
        url = f"{self.base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                resp_data = resp.read()
                return json.loads(resp_data)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(
                f"Ollama API HTTP error {e.code}: {e.reason}. Response: {error_body}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to connect to Ollama at {self.base_url}: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to decode JSON response from Ollama: {e}") from e

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        template: Optional[str] = None,
        context: Optional[List[int]] = None,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        raw: bool = False,
        keep_alive: Optional[str] = None,
    ) -> str:
        """
        Generate a completion from the model.

        Args:
            prompt: The prompt to send to the model.
            system: Optional system message to override the model's system prompt.
            template: Optional template string to use for formatting.
            context: Optional list of token IDs representing the conversation context.
            options: Optional dict of model parameters (temperature, top_p, etc.).
            stream: If True, the response will be streamed (not implemented; returns full response).
            raw: If True, no formatting is applied to the prompt.
            keep_alive: Controls how long the model stays loaded (e.g., "5m", "2h").

        Returns:
            The generated text response.
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "raw": raw,
        }
        if system is not None:
            payload["system"] = system
        if template is not None:
            payload["template"] = template
        if context is not None:
            payload["context"] = context
        if options is not None:
            payload["options"] = options
        if keep_alive is not None:
            payload["keep_alive"] = keep_alive

        # Ollama's /api/generate endpoint returns a streaming response when stream=True.
        # For simplicity, we disable streaming and get the full response.
        payload["stream"] = False

        response = self._make_request("/api/generate", payload)
        # The response format includes a "response" field with the generated text.
        return response.get("response", "")

    def chat(
        self,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        keep_alive: Optional[str] = None,
    ) -> str:
        """
        Send a chat conversation to the model (uses /api/chat endpoint).

        Args:
            messages: List of message dicts with keys "role" and "content".
                      Roles: "system", "user", "assistant".
            options: Optional dict of model parameters.
            stream: If True, stream the response (not implemented).
            keep_alive: Controls how long the model stays loaded.

        Returns:
            The model's response as a string.
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
        }
        if options is not None:
            payload["options"] = options
        if keep_alive is not None:
            payload["keep_alive"] = keep_alive

        payload["stream"] = False  # Disable streaming for simplicity

        response = self._make_request("/api/chat", payload)
        # The chat endpoint returns a message object under "message"
        message = response.get("message", {})
        return message.get("content", "")

    def list_models(self) -> List[str]:
        """
        Retrieve a list of available models from the Ollama instance.

        Returns:
            List of model names.
        """
        response = self._make_request("/api/tags", {})
        models = response.get("models", [])
        return [m.get("name", "") for m in models if m.get("name")]

    def show_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Show detailed information about a specific model.

        Args:
            model_name: Name of the model to inspect. If None, uses the client's default model.

        Returns:
            Dictionary containing model details.
        """
        model = model_name if model_name is not None else self.model
        payload = {"name": model}
        return self._make_request("/api/show", payload)