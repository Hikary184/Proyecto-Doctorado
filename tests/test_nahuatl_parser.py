from src.importers.parsers.nahuatl_txt import (
    parse_headword
)


def test_simple_headword():

    headword, sense = parse_headword(
        "aakatl"
    )

    assert headword == "aakatl"

    assert sense is None


def test_numbered_sense():

    headword, sense = parse_headword(
        "aaki 2"
    )

    assert headword == "aaki"

    assert sense == 2


def test_multiword_headword():

    headword, sense = parse_headword(
        "achi kuali"
    )

    assert headword == "achi kuali"

    assert sense is None


def test_prefix_headword():

    headword, sense = parse_headword(
        "a-"
    )

    assert headword == "a-"

    assert sense is None


def test_question_headword():

    headword, sense = parse_headword(
        "¿kanin ka?"
    )

    assert headword == "¿kanin ka?"

    assert sense is None