"""Tests for Gemini provider."""

import json
from unittest.mock import MagicMock, patch

from commit_with_ai.providers.base import BaseProvider
from commit_with_ai.providers.gemini import GeminiProvider


class TestGeminiProvider:
    def test_is_base_provider_subclass(self):
        assert issubclass(GeminiProvider, BaseProvider)

    def test_default_model(self):
        provider = GeminiProvider()
        assert provider.default_model == "gemini-3-flash-preview"

    def test_custom_model(self):
        provider = GeminiProvider(model="gemini-2.0-flash")
        assert provider.model == "gemini-2.0-flash"

    @patch("commit_with_ai.providers.gemini.genai")
    def test_generate_commit_messages_returns_list(self, mock_genai):
        messages_data = {
            "messages": [
                {
                    "type": "feat",
                    "scope": "",
                    "description": "add feature",
                    "full_message": "feat: add feature",
                }
            ]
            * 5
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(messages_data)
        mock_genai.Client.return_value.models.generate_content.return_value = mock_response

        provider = GeminiProvider()
        result = provider.generate_commit_messages("diff content")

        assert len(result) == 5
        assert result[0]["type"] == "feat"
        assert result[0]["full_message"] == "feat: add feature"

    def test_requires_api_key_env(self):
        provider = GeminiProvider()
        assert hasattr(provider, "generate_commit_messages")
