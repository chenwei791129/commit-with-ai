"""Tests for Claude CLI provider."""

import json
import subprocess
from unittest.mock import patch, MagicMock

import pytest

from commit_with_ai.providers.base import BaseProvider
from commit_with_ai.providers.claude_cli import ClaudeCliProvider


class TestClaudeCliProviderInit:
    def test_is_base_provider_subclass(self):
        assert issubclass(ClaudeCliProvider, BaseProvider)

    def test_default_model_is_haiku(self):
        with patch(
            "commit_with_ai.providers.claude_cli.shutil.which", return_value="/usr/bin/claude"
        ):
            provider = ClaudeCliProvider()
        assert provider.default_model == "haiku"

    def test_custom_model(self):
        with patch(
            "commit_with_ai.providers.claude_cli.shutil.which", return_value="/usr/bin/claude"
        ):
            provider = ClaudeCliProvider(model="sonnet")
        assert provider.model == "sonnet"


class TestClaudeCliAvailabilityCheck:
    def test_raises_when_claude_not_found(self):
        with patch("commit_with_ai.providers.claude_cli.shutil.which", return_value=None):
            with pytest.raises(SystemExit):
                ClaudeCliProvider()

    def test_succeeds_when_claude_found(self):
        with patch(
            "commit_with_ai.providers.claude_cli.shutil.which", return_value="/usr/bin/claude"
        ):
            provider = ClaudeCliProvider()
        assert provider is not None


class TestClaudeCliGenerateMessages:
    def _make_provider(self):
        with patch(
            "commit_with_ai.providers.claude_cli.shutil.which", return_value="/usr/bin/claude"
        ):
            return ClaudeCliProvider()

    def test_subprocess_includes_no_session_persistence_flag(self):
        provider = self._make_provider()
        cli_output = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "result": "",
                "structured_output": {
                    "messages": [
                        {
                            "type": "feat",
                            "scope": "",
                            "description": f"change {i}",
                            "full_message": f"feat: change {i}",
                        }
                        for i in range(5)
                    ]
                },
            }
        )

        with patch("commit_with_ai.providers.claude_cli.subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout=cli_output, stderr=""
            )
            provider.generate_commit_messages("diff content")

        args_list = mock_run.call_args[0][0]
        assert "--no-session-persistence" in args_list

    def test_prompt_passed_via_stdin_not_positional_arg(self):
        provider = self._make_provider()
        cli_output = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "result": "",
                "structured_output": {
                    "messages": [
                        {
                            "type": "feat",
                            "scope": "",
                            "description": f"change {i}",
                            "full_message": f"feat: change {i}",
                        }
                        for i in range(5)
                    ]
                },
            }
        )

        with patch("commit_with_ai.providers.claude_cli.subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout=cli_output, stderr=""
            )
            provider.generate_commit_messages("diff content")

        # Prompt should be passed via input kwarg, not as positional arg
        kwargs = mock_run.call_args[1]
        assert "input" in kwargs
        assert "diff content" in kwargs["input"]
        # Prompt should not appear in the command args list
        args_list = mock_run.call_args[0][0]
        for arg in args_list:
            assert "diff content" not in arg

    def test_successful_generation(self):
        provider = self._make_provider()
        messages_data = {
            "messages": [
                {
                    "type": "feat",
                    "scope": "",
                    "description": f"change {i}",
                    "full_message": f"feat: change {i}",
                }
                for i in range(5)
            ]
        }
        cli_output = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "result": "",
                "structured_output": messages_data,
            }
        )

        with patch("commit_with_ai.providers.claude_cli.subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout=cli_output, stderr=""
            )
            result = provider.generate_commit_messages("diff content")

        assert len(result) == 5
        assert result[0]["type"] == "feat"
        assert result[0]["full_message"] == "feat: change 0"

    def test_cli_non_zero_exit(self):
        provider = self._make_provider()

        with patch("commit_with_ai.providers.claude_cli.subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=[], returncode=1, stdout="", stderr="auth error"
            )
            with pytest.raises(SystemExit):
                provider.generate_commit_messages("diff content")

    def test_invalid_json_output(self):
        provider = self._make_provider()

        with patch("commit_with_ai.providers.claude_cli.subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="not json", stderr=""
            )
            with pytest.raises(SystemExit):
                provider.generate_commit_messages("diff content")
