import json
import os
import sys
import time
from typing import Optional, List, Dict, Any
from config import Config, load
from prompts import get_prompt_for_command
from history_manager import HistoryManager
from ollama_client import OllamaClient
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
from rich import box
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner

class GameForgeCLI:
    """Main GameForge CLI application with interactive interface and slash commands."""
    
    def __init__(self) -> None:
        self.config = load()
        self.console = Console()
        self.history = HistoryManager(max_tokens=self.config.get("history_limit", 20))
        self.ollama = OllamaClient(
            base_url=self.config.get("endpoint"),
            model=self.config.get("model")
        )
        self.current_command: Optional[str] = None
        self.show_thinking = self.config.get("show_thinking", False)
        
    def run(self) -> None:
        """Main application loop."""
        self.console.print(Panel(
            f"[bold green]GameForge CLI[/bold green] - AI-powered game development assistant\n"
            f"[dim]Local, offline, and ready to help with your game projects[/dim]",
            border_style="green"
        ))
        
        self.console.print("\nType [bold green]/help[/bold green] for available commands or start describing your game development needs.")
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]", console=self.console)
                
                if user_input.startswith("/"):
                    self.handle_command(user_input)
                else:
                    self.handle_user_message(user_input)
                    
            except (KeyboardInterrupt, EOFError):
                self.console.print("\n[bold yellow]Goodbye! Happy game developing![/bold yellow]")
                break
    
    def handle_command(self, command: str) -> None:
        """Process slash commands."""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == "/help":
            self.show_help()
        elif cmd == "/clear":
            self.clear_history()
        elif cmd == "/models":
            self.list_models()
        elif cmd == "/model":
            self.set_model(" ".join(parts[1:]) if len(parts) > 1 else "")
        elif cmd == "/config":
            self.show_config()
        elif cmd == "/exit" or cmd == "/quit":
            self.console.print("\n[bold yellow]Goodbye! Happy game developing![/bold yellow]")
            sys.exit(0)
        else:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            self.console.print("Type [bold green]/help[/bold green] for available commands.")
    
    def handle_user_message(self, message: str) -> None:
        """Process regular user messages and generate AI responses."""
        if not message.strip():
            return
        
        self.history.add_message("user", message)
        self.current_command = self.detect_command(message)
        
        prompt = get_prompt_for_command(
            self.current_command or "general",
            message,
            self.history.get_history()
        )
        
        self.console.print(f"\n[bold blue]GameForge[/bold blue]: Thinking...", style="dim")
        
        response = self.generate_response(prompt)
        
        if response:
            self.history.add_message("assistant", response)
            self.display_response(response)
    
    def detect_command(self, message: str) -> Optional[str]:
        """Detect if the message contains a command keyword."""
        message_lower = message.lower()
        commands = ["generate code", "fix bug", "suggest asset", "design game"]
        
        for cmd in commands:
            if cmd in message_lower:
                return cmd.replace(" ", "_")
        
        return None
    
    def generate_response(self, prompt: str) -> Optional[str]:
        """Generate AI response using Ollama client."""
        try:
            if self.show_thinking:
                with Live(console=self.console, refresh_per_second=4) as live:
                    live.update(Spinner("dots", text="Generating response..."))
                    response = self.ollama.chat(prompt)
                return response
            else:
                return self.ollama.chat(prompt)
        except Exception as e:
            self.console.print(f"[red]Error generating response: {e}[/red]")
            return None
    
    def display_response(self, response: str) -> None:
        """Display AI response with proper formatting."""
        self.console.print(f"\n[bold blue]GameForge[/bold blue]:")
        
        # Parse response for code blocks
        if response.strip().startswith("```"):
            # Code response
            code_blocks = self.extract_code_blocks(response)
            for i, (lang, code) in enumerate(code_blocks):
                self.console.print(f"\n[bold]Code Block {i+1}:[/bold] [dim]({lang or 'text'})[/dim]")
                self.console.print("\n" + code + "\n")
        else:
            # Regular text response with markdown
            md = Markdown(response)
            self.console.print(md)
    
    def extract_code_blocks(self, text: str) -> List[tuple[Optional[str], str]]:
        """Extract code blocks from text with optional language identifiers."""
        blocks = []
        lines = text.split("\n")
        in_code_block = False
        current_lang = None
        current_code = []
        
        for line in lines:
            if line.startswith("```"):
                if in_code_block:
                    # End of code block
                    blocks.append((current_lang, "\n".join(current_code)))
                    current_code = []
                    current_lang = None
                    in_code_block = False
                else:
                    # Start of code block
                    parts = line[3:].strip().split()
                    current_lang = parts[0] if parts else None
                    in_code_block = True
            elif in_code_block:
                current_code.append(line)
        
        return blocks
    
    def show_help(self) -> None:
        """Display help information."""
        help_text = """
        [bold green]GameForge CLI Help[/bold green]

        [bold]Available Commands:[/bold]
        /help        - Show this help message
        /clear       - Clear conversation history
        /models      - List available Ollama models
        /model <name> - Set the AI model to use
        /config      - Show current configuration
        /exit        - Exit the application

        [bold]Usage Examples:[/bold]
        • "Generate a Pygame script for a platformer game"
        • "Fix the bug in my Unity C# script"
        • "Suggest pixel art assets for a fantasy RPG"
        • "Design a mobile puzzle game concept"

        [bold]Tips:[/bold]
        • Be specific about your requirements
        • Mention your preferred game engine or framework
        • Ask for code examples, asset suggestions, or game design ideas
        • Use /clear to start fresh conversations
        """
        self.console.print(help_text)
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.history.clear()
        self.console.print("[green]Conversation history cleared.[/green]")
    
    def list_models(self) -> None:
        """List available Ollama models."""
        try:
            models = self.ollama.list_models()
            table = Table(title="Available Models", box=box.SIMPLE)
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Size", style="green")
            
            for model in models:
                table.add_row(model["name"], model["size"])
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error listing models: {e}[/red]")
    
    def set_model(self, model_name: str) -> None:
        """Set the AI model to use."""
        if not model_name:
            self.console.print("[red]Please specify a model name.[/red]")
            return
        
        try:
            self.ollama.model = model_name
            self.config.set("model", model_name)
            self.config.save()
            self.console.print(f"[green]Model set to: {model_name}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error setting model: {e}[/red]")
    
    def show_config(self) -> None:
        """Display current configuration."""
        config_data = self.config.as_dict()
        table = Table(title="Current Configuration", box=box.ROUNDED)
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in config_data.items():
            table.add_row(key, str(value))
        
        self.console.print(table)

def main() -> None:
    """Entry point for GameForge CLI."""
    cli = GameForgeCLI()
    cli.run()

if __name__ == "__main__":
    main()