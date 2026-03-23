"""Base provider interface for AI commit message generation."""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Abstract base class for AI providers.

    Each provider must implement generate_commit_messages and define a default_model.
    """

    default_model: str = ""

    @abstractmethod
    def generate_commit_messages(self, diff_content: str) -> list[dict[str, str]]:
        """Generate commit messages from a git diff.

        Args:
            diff_content: The git diff string to analyze.

        Returns:
            A list of exactly 5 commit message dicts, each with keys:
            type, scope, description, full_message.
        """
