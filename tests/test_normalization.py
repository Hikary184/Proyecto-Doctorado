from src.normalization.normalizer import (
    normalize_form
)


def test_lowercase_normalization():

    result = normalize_form(
        "EXAMPLE"
    )

    assert result.normalized_form == "example"


def test_whitespace_normalization():

    result = normalize_form(
        "   example    word   "
    )

    assert result.normalized_form == "example word"


def test_diacritics_are_preserved():

    result = normalize_form(
        "ÁRBOL"
    )

    assert result.normalized_form == "árbol"


def test_unicode_composition():

    decomposed = "a\u0301"

    result = normalize_form(
        decomposed
    )

    assert result.normalized_form == "á"


def test_original_string_is_not_modified():

    original = "  EXAMPLE  "

    result = normalize_form(
        original
    )

    assert original == "  EXAMPLE  "

    assert result.normalized_form == "example"