"""Tests for core module: git operations, menu display, and commit flow."""

import subprocess
from unittest.mock import patch

from commit_with_ai.core import check_staged_changes, get_staged_diff, run_command


class TestRunCommand:
    def test_successful_command(self):
        result = run_command(["echo", "hello"])
        assert result.returncode == 0
        assert result.stdout.strip() == "hello"

    def test_failed_command_with_check_raises(self):
        with patch("sys.exit") as mock_exit:
            run_command(["false"], check=True)
            mock_exit.assert_called_once_with(1)

    def test_failed_command_without_check(self):
        result = run_command(["false"], check=False)
        assert result.returncode != 0


class TestCheckStagedChanges:
    def test_no_staged_changes(self):
        with patch("commit_with_ai.core.run_command") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
            assert check_staged_changes() is False

    def test_has_staged_changes(self):
        with patch("commit_with_ai.core.run_command") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1)
            assert check_staged_changes() is True


class TestGetStagedDiff:
    def test_returns_diff_content(self):
        with patch("commit_with_ai.core.run_command") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="diff content here"
            )
            assert get_staged_diff() == "diff content here"
