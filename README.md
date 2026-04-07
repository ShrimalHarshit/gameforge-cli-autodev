# 🎮 GameForge CLI
> A local, offline AI-powered game development assistant that runs entirely on your machine using Ollama.

## ✨ Features
- **🔒 100% Offline & Private:** Runs locally with zero external API calls or cloud dependencies.
- **📦 Zero External Dependencies:** Built exclusively with Python's standard library (`http.client`, `json`, `os`, `sys`). No `pip install` required.
- **⚡ Interactive Slash Commands:** Streamlined workflow with `/code`, `/fix`, `/assets`, `/design`, `/clear`, and `/help`.
- **🧠 Smart Context Management:** Maintains session history with automatic context window trimming to prevent token overflow.
- **🖥️ Terminal-Optimized Rendering:** AI responses are parsed and formatted for clean, readable output directly in your terminal.
- **⚙️ Fully Configurable:** Easily switch models, adjust endpoints, and tune context limits via a simple JSON config file.

## 📋 Prerequisites
- **Python 3.8+** (Standard library only)
- **Ollama** installed and running locally (`ollama serve`)
- At least one Ollama model pulled (e.g., `ollama pull llama3`, `ollama pull codellama`, `ollama pull mistral`)

## 🚀 Quick Start
1. Ensure Ollama is running in the background:
   ```bash
   ollama serve
   ```
2. Clone or download the GameForge CLI repository.
3. Run the application:
   ```bash
   python main.py
   ```
4. Start interacting! Type `/help` to see available commands.

## ⚙️ Configuration
GameForge CLI uses a `config.json` file in the root directory. If it doesn't exist, the CLI will generate a default one on first run.

```json
{
  "ollama_endpoint": "http://localhost:11434",
  "model": "llama3",
  "context_window": 4096,
  "max_history_messages": 10,
  "temperature": 0.7,
  "stream_response": true
}
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ollama_endpoint` | Local Ollama API URL | `http://localhost:11434` |
| `model` | Ollama model to use | `llama3` |
| `context_window` | Max tokens for context trimming | `4096` |
| `max_history_messages` | Number of messages to keep in history | `10` |
| `temperature` | AI creativity/randomness | `0.7` |
| `stream_response` | Enable real-time token streaming | `true` |

## 💻 Usage & Commands
Once launched, you'll enter an interactive prompt. Use the following slash commands to control the assistant:

| Command | Description |
|---------|-------------|
| `/code <prompt>` | Generate game code (Python, C#, GDScript, etc.) |
| `/fix <prompt>` | Debug and fix provided code snippets |
| `/assets <prompt>` | Suggest or describe game assets, sprites, and audio |
| `/design <prompt>` | Brainstorm game mechanics, levels, and lore |
| `/clear` | Clear conversation history and reset context |
| `/help` | Display available commands and usage tips |
| `/exit` or `/quit` | Gracefully exit the CLI |

**Example Session:**
```text
🎮 GameForge CLI v1.0.0 | Model: llama3 | Endpoint: http://localhost:11434
Type /help for commands. Press Ctrl+C to exit.

> /code Create a simple player movement script in GDScript for Godot 4
🤖 Generating code...
extends CharacterBody2D

@export var speed = 400.0

func _physics_process(delta):
    var input_vector = Vector2.ZERO
    input_vector.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
    input_vector.y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")
    input_vector = input_vector.normalized()

    velocity = input_vector * speed
    move_and_slide()

> /fix The player slides on ice. How do I add friction?
🤖 Analyzing code...
To add friction, you can modify the velocity when no input is detected...
```

## 📁 Project Structure
```
gameforge-cli/
├── main.py              # Entry point & CLI loop
├── gameforge_cli.py     # Core CLI logic & command routing
├── ollama_client.py     # Standard library HTTP client for Ollama API
├── history_manager.py   # Session history & context window trimming
├── prompts.py           # System prompts & command templates
├── config.py            # Configuration loader & validator
└── config.json          # User configuration (auto-generated)
```

## 🛠️ Architecture Notes
- **Zero Dependencies:** All HTTP communication with Ollama is handled via `http.client` and `json` from Python's standard library.
- **Context Trimming:** `history_manager.py` dynamically calculates token usage and trims older messages when the `context_window` limit is approached, ensuring stable performance.
- **Streaming Support:** Responses are streamed token-by-token for a responsive, real-time terminal experience.
- **Markdown Parsing:** Built-in lightweight parser converts AI markdown output into terminal-friendly formatting (code blocks, lists, headers) without external libraries.

## 🤝 Contributing
Contributions are welcome! Since this project uses only the standard library, it's an excellent starting point for learning Python networking, CLI design, and LLM integration.
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ for offline game developers. Powered by Ollama & Python Standard Library.*