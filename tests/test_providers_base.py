"""Tests for provider base class interface contract."""

import pytest

from commit_with_ai.providers.base import BaseProvider


class TestBaseProvider:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            BaseProvider()

    def test_subclass_must_implement_generate(self):
        class IncompleteProvider(BaseProvider):
            pass

        with pytest.raises(TypeError):
            IncompleteProvider()

    def test_subclass_with_generate_can_instantiate(self):
        class ConcreteProvider(BaseProvider):
            def generate_commit_messages(self, diff_content: str) -> list[dict[str, str]]:
                return []

        provider = ConcreteProvider()
        assert provider.generate_commit_messages("") == []

    def test_default_model_is_none(self):
        class ConcreteProvider(BaseProvider):
            default_model = "test-model"

            def generate_commit_messages(self, diff_content: str) -> list[dict[str, str]]:
                return []

        provider = ConcreteProvider()
        assert provider.default_model == "test-model"
