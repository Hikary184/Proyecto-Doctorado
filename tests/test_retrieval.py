from src.models.lexical_entry import (
    LexicalEntry
)

from src.normalization.normalizer import (
    normalize_form
)

from src.retrieval.exact import (
    search_exact_raw,
    search_exact_normalized
)

from src.retrieval.fuzzy import (
    search_fuzzy_normalized
)


def create_entry(
    entry_id: str,
    headword: str
):

    entry = LexicalEntry(
        id=entry_id,

        language={
            "name": "test_language"
        },

        headword=headword
    )

    entry.computational_analysis.normalization = (
        normalize_form(
            headword
        )
    )

    return entry


ENTRIES = [

    create_entry(
        "test-001",
        "Example"
    ),

    create_entry(
        "test-002",
        "House"
    ),

    create_entry(
        "test-003",
        "Árbol"
    )
]


def test_exact_raw():

    results = search_exact_raw(
        "Example",
        ENTRIES
    )

    assert len(results) == 1

    assert (
        results[0].entry_id
        == "test-001"
    )


def test_exact_raw_is_case_sensitive():

    results = search_exact_raw(
        "example",
        ENTRIES
    )

    assert len(results) == 0


def test_exact_normalized():

    results = (
        search_exact_normalized(
            " EXAMPLE ",
            ENTRIES
        )
    )

    assert len(results) == 1

    assert (
        results[0].entry_id
        == "test-001"
    )


def test_fuzzy_typo():

    results = (
        search_fuzzy_normalized(
            "exampel",
            ENTRIES,
            top_k=1
        )
    )

    assert len(results) == 1

    assert (
        results[0].entry_id
        == "test-001"
    )


def test_diacritic_not_removed():

    results = (
        search_exact_normalized(
            "arbol",
            ENTRIES
        )
    )

    assert len(results) == 0