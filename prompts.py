from typing import List, Dict, Optional
from config import Config

def _get_base_system_prompt() -> str:
    """Returns the core system prompt that defines the assistant's behavior."""
    return (
        "You are GameForge, an AI-powered game development assistant that runs entirely offline. "
        "You help users with code generation, debugging, asset suggestions, and game design. "
        "You are knowledgeable about popular game engines (Unity, Godot, Unreal) and frameworks (Pygame, Pyglet, Arcade). "
        "Provide clear, concise, and actionable advice. When generating code, follow best practices and include necessary imports. "
        "When suggesting assets, describe style, format, and usage. When fixing bugs, explain the issue and provide a corrected version. "
        "When designing games, outline mechanics, story, and technical considerations. Always respond in a helpful and friendly tone."
    )

def get_code_generation_prompt(user_request: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Builds a prompt for generating code based on a user request.
    :param user_request: The user's description of the desired code.
    :param conversation_history: Optional list of previous exchanges for context.
    :return: A fully formed prompt string.
    """
    system_prompt = _get_base_system_prompt()
    history_section = ""
    if conversation_history:
        history_section = "\n\nConversation history:\n"
        for exchange in conversation_history:
            role = exchange.get("role", "user").capitalize()
            content = exchange.get("content", "")
            history_section += f"{role}: {content}\n"
    prompt = (
        f"{system_prompt}{history_section}\n\n"
        f"User request: Generate code for the following:\n{user_request}\n\n"
        "Please provide the complete code snippet, including necessary imports and comments explaining key parts."
    )
    return prompt

def get_bug_fixing_prompt(code_snippet: str, error_description: str,
                          conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Builds a prompt for fixing a bug in provided code.
    :param code_snippet: The code that exhibits the bug.
    :param error_description: Description of the error or unexpected behavior.
    :param conversation_history: Optional list of previous exchanges for context.
    :return: A fully formed prompt string.
    """
    system_prompt = _get_base_system_prompt()
    history_section = ""
    if conversation_history:
        history_section = "\n\nConversation history:\n"
        for exchange in conversation_history:
            role = exchange.get("role", "user").capitalize()
            content = exchange.get("content", "")
            history_section += f"{role}: {content}\n"
    prompt = (
        f"{system_prompt}{history_section}\n\n"
        f"The user provided the following code that contains a bug:\n```\n{code_snippet}\n```\n\n"
        f"Error description or observed behavior:\n{error_description}\n\n"
        "Please identify the bug, explain why it occurs, and provide a corrected version of the code."
    )
    return prompt

def get_asset_suggestion_prompt(asset_type: str, description: str,
                                conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Builds a prompt for suggesting game assets.
    :param asset_type: Type of asset (e.g., 'sprite', 'sound effect', '3D model').
    :param description: User's description of the desired asset.
    :param conversation_history: Optional list of previous exchanges for context.
    :return: A fully formed prompt string.
    """
    system_prompt = _get_base_system_prompt()
    history_section = ""
    if conversation_history:
        history_section = "\n\nConversation history:\n"
        for exchange in conversation_history:
            role = exchange.get("role", "user").capitalize()
            content = exchange.get("content", "")
            history_section += f"{role}: {content}\n"
    prompt = (
        f"{system_prompt}{history_section}\n\n"
        f"User wants suggestions for a {asset_type} asset with the following description:\n{description}\n\n"
        "Please suggest specific asset ideas, including style, format (e.g., PNG, SVG, WAV), approximate dimensions, "
        "and where they could be sourced or how they could be created."
    )
    return prompt

def get_game_design_prompt(core_idea: str,
                           conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Builds a prompt for assisting with game design.
    :param core_idea: The user's central game idea or concept.
    :param conversation_history: Optional list of previous exchanges for context.
    :return: A fully formed prompt string.
    """
    system_prompt = _get_base_system_prompt()
    history_section = ""
    if conversation_history:
        history_section = "\n\nConversation history:\n"
        for exchange in conversation_history:
            role = exchange.get("role", "user").capitalize()
            content = exchange.get("content", "")
            history_section += f"{role}: {content}\n"
    prompt = (
        f"{system_prompt}{history_section}\n\n"
        f"User wants help designing a game based on the following idea:\n{core_idea}\n\n"
        "Please outline core gameplay mechanics, story/narrative elements, art style, "
        "technical considerations (engine, language), and a rough development roadmap."
    )
    return prompt

def get_prompt_for_command(command: str, **kwargs) -> str:
    """
    Dispatches to the appropriate prompt builder based on the slash command.
    :param command: The command string (e.g., '/generate', '/fix', '/assets', '/design').
    :param kwargs: Arguments required by the specific prompt builder.
    :return: A fully formed prompt string.
    :raises ValueError: If an unknown command is provided.
    """
    if command == "/generate":
        return get_code_generation_prompt(
            user_request=kwargs.get("user_request", ""),
            conversation_history=kwargs.get("conversation_history")
        )
    elif command == "/fix":
        return get_bug_fixing_prompt(
            code_snippet=kwargs.get("code_snippet", ""),
            error_description=kwargs.get("error_description", ""),
            conversation_history=kwargs.get("conversation_history")
        )
    elif command == "/assets":
        return get_asset_suggestion_prompt(
            asset_type=kwargs.get("asset_type", ""),
            description=kwargs.get("description", ""),
            conversation_history=kwargs.get("conversation_history")
        )
    elif command == "/design":
        return get_game_design_prompt(
            core_idea=kwargs.get("core_idea", ""),
            conversation_history=kwargs.get("conversation_history")
        )
    else:
        raise ValueError(f"Unknown command '{command}' for prompt generation.")