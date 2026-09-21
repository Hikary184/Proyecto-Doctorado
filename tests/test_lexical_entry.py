import pytest
from pydantic import ValidationError

from src.models.lexical_entry import (
    LexicalEntry
)


def test_minimal_entry():

    data = {
        "id": "test-001",

        "language": {
            "name": "test_language"
        },

        "headword": "example"
    }

    entry = LexicalEntry.model_validate(data)

    assert entry.id == "test-001"

    assert entry.headword == "example"

    assert entry.language.name == "test_language"


def test_missing_headword():

    data = {
        "id": "test-002",

        "language": {
            "name": "test_language"
        }
    }

    with pytest.raises(ValidationError):

        LexicalEntry.model_validate(data)