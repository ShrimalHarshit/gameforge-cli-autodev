import sys
from typing import NoReturn

def main() -> int:
    """
    Entry point for the GameForge CLI application.

    Initializes the CLI, runs the interactive session, and handles
    graceful shutdown on user interruption or unexpected errors.

    Returns:
        int: Exit status code (0 for success, non-zero for failure).
    """
    try:
        # Delay import to allow early error reporting if the module is missing
        from gameforge_cli import GameForgeCLI

        cli = GameForgeCLI()
        cli.run()
        return 0

    except KeyboardInterrupt:
        # User-initiated interruption (Ctrl+C)
        sys.stderr.write("\n\nSession interrupted. Goodbye!\n")
        return 0

    except (ImportError, ModuleNotFoundError) as e:
        # Failed to load the core CLI module
        sys.stderr.write(f"\nImport Error: {e}\n")
        sys.stderr.write(
            "Please ensure all project files are present in the same directory "
            "and that the environment is correctly set up.\n"
        )
        return 1

    except Exception as e:
        # Catch-all for any other unexpected errors
        sys.stderr.write(f"\nFatal Error: {type(e).__name__}: {e}\n")
        sys.stderr.write(
            "An unexpected error occurred. Please report this issue "
            "with the full traceback if possible.\n"
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())