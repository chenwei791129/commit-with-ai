#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "google-genai>=1.60.0",
# ]
# ///
"""Git auto-commit with AI-generated commit messages using structured JSON output."""

import json
import os
import subprocess
import sys
from typing import List, Dict
from google import genai


def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if check and result.returncode != 0:
        print(f"❌ Command failed: {' '.join(cmd)}")
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


def generate_commit_messages(diff_content: str) -> List[Dict[str, str]]:
    """Generate commit messages using Gemini API with structured JSON output."""
    client = genai.Client()

    # Define schema for commit message output
    response_schema = {
        "type": "object",
        "properties": {
            "messages": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "scope": {"type": "string"},
                        "description": {"type": "string"},
                        "full_message": {"type": "string"},
                    },
                    "required": ["type", "description", "full_message"],
                },
                "minItems": 5,
                "maxItems": 5,
            }
        },
        "required": ["messages"],
    }

    prompt = f"""Analyze the following git diff and generate 5 distinct, concise, and descriptive commit messages.

Requirements:
1. MUST strictly follow the Conventional Commits specification
2. Format: <type>(<scope>): <description>
   - type: feat, fix, docs, style, refactor, test, chore, etc.
   - scope: optional, can be empty string if not applicable
   - description: concise description in imperative mood
3. MUST be written in English
4. Each message should offer a different perspective or level of detail
5. Keep descriptions under 72 characters

Git diff:
{diff_content}

Output a JSON object with a "messages" array containing exactly 5 commit message objects.
Each object should have: type, scope (empty string if N/A), description, and full_message."""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            },
        )

        data = json.loads(response.text)
        return data["messages"]

    except Exception as e:
        print(f"❌ Failed to generate commit messages: {e}")
        sys.exit(1)


def display_menu(messages: List[Dict[str, str]]) -> None:
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


def get_user_selection(messages: List[Dict[str, str]]) -> str:
    """Get user's commit message selection."""
    while True:
        try:
            choice = input("\nEnter selection [1-7]: ").strip()

            if choice == "7":
                print("Commit cancelled.")
                sys.exit(0)
            elif choice == "6":
                custom_msg = input("Enter custom commit message: ").strip()
                if custom_msg:
                    return custom_msg
                else:
                    print("❌ Commit message cannot be empty.")
                    continue
            elif choice in ["1", "2", "3", "4", "5"]:
                idx = int(choice) - 1
                return messages[idx]["full_message"]
            else:
                print("❌ Invalid selection. Please enter 1-7.")
        except (ValueError, KeyboardInterrupt):
            print("\nCommit cancelled.")
            sys.exit(0)


def commit_changes(message: str) -> None:
    """Commit staged changes with the given message."""
    print(f"\nCommitting with message: {message}")
    run_command(["git", "commit", "-m", message])
    print("✓ Commit successful!")


def main():
    """Main function."""
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY or GOOGLE_API_KEY not set")
        print("Please set one of these environment variables with your API key")
        sys.exit(1)

    # Check for staged changes
    if not check_staged_changes():
        print("❌ No staged changes found. Please stage your changes first.")
        print("\nTip: Use 'git add <files>' to stage changes")
        sys.exit(1)

    # Get staged diff
    print("Analyzing staged changes...")
    diff_content = get_staged_diff()

    # Generate commit messages
    print("Generating commit message options with Gemini API...")
    messages = generate_commit_messages(diff_content)

    # Display menu and get selection
    display_menu(messages)
    selected_message = get_user_selection(messages)

    # Commit changes
    commit_changes(selected_message)


if __name__ == "__main__":
    main()
