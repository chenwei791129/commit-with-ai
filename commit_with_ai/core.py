"""Core logic for commit-with-ai: git operations, menu, and commit flow."""

import readline  # noqa: F401 - Side effect import: enables readline editing in input()
import subprocess
import sys
import termios
import tty


def getch() -> str:
    """Read a single character from stdin without requiring Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if check and result.returncode != 0:
        print(f"Error: Command failed: {' '.join(cmd)}")
        print(f"Error: {result.stderr}")
        sys.exit(1)

    return result


def check_staged_changes() -> bool:
    """Check if there are staged changes."""
    result = run_command(["git", "diff", "--cached", "--quiet"], check=False)
    return result.returncode != 0


def get_staged_diff() -> str:
    """Get the diff of staged changes."""
    result = run_command(["git", "diff", "--cached"])
    return result.stdout


def display_menu(messages: list[dict[str, str]]) -> None:
    """Display commit message options."""
    print("\n" + "=" * 70)
    print("Select a commit message:")
    print("=" * 70)

    for i, msg in enumerate(messages, 1):
        scope_part = f"({msg['scope']})" if msg.get("scope") else ""
        print(f"{i}. {msg['type']}{scope_part}: {msg['description']}")
        if msg["full_message"] != f"{msg['type']}{scope_part}: {msg['description']}":
            print(f"   Full: {msg['full_message']}")

    print("6. Enter custom message")
    print("7. Cancel")
    print("=" * 70)


def get_user_selection(messages: list[dict[str, str]]) -> str:
    """Get user's commit message selection."""
    print("\nEnter selection [1-7]: ", end="", flush=True)

    while True:
        try:
            choice = getch()

            if choice == "\x03":
                print("\nCommit cancelled.")
                sys.exit(0)

            if choice == "7":
                print(choice)
                print("Commit cancelled.")
                sys.exit(0)
            elif choice == "6":
                print(choice)
                custom_msg = input("Enter custom commit message: ").strip()
                if custom_msg:
                    return custom_msg
                else:
                    print("Error: Commit message cannot be empty.")
                    print("Enter selection [1-7]: ", end="", flush=True)
                    continue
            elif choice in ["1", "2", "3", "4", "5"]:
                print(choice)
                idx = int(choice) - 1
                return messages[idx]["full_message"]
            else:
                continue
        except (ValueError, KeyboardInterrupt):
            print("\nCommit cancelled.")
            sys.exit(0)


def commit_changes(message: str) -> None:
    """Commit staged changes with the given message."""
    print(f"\nCommitting with message: {message}")
    run_command(["git", "commit", "-m", message])
    print("Commit successful!")


def main():
    """Main entry point - placeholder, will be replaced by __main__.py logic."""
    pass
