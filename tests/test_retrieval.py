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

from src.retrieval.cascade import (
    search_cascade
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


# ============================================================
# B0 - EXACT RAW
# ============================================================


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


# ============================================================
# B1 - EXACT NORMALIZED
# ============================================================


def test_exact_normalized():

    results = search_exact_normalized(
        " EXAMPLE ",
        ENTRIES
    )

    assert len(results) == 1

    assert (
        results[0].entry_id
        == "test-001"
    )


def test_diacritic_not_removed():

    results = search_exact_normalized(
        "arbol",
        ENTRIES
    )

    assert len(results) == 0


# ============================================================
# B2 - FUZZY NORMALIZED
# ============================================================


def test_fuzzy_typo():

    results = search_fuzzy_normalized(
        "exampel",
        ENTRIES,
        top_k=1
    )

    assert len(results) == 1

    assert (
        results[0].entry_id
        == "test-001"
    )


# ============================================================
# B3 - CASCADED RETRIEVAL
# ============================================================


def test_cascade_prefers_exact_raw():

    results = search_cascade(
        "Example",
        ENTRIES
    )

    assert results

    assert (
        results[0].headword
        == "Example"
    )


def test_cascade_uses_normalized():

    results = search_cascade(
        "EXAMPLE",
        ENTRIES
    )

    assert results

    assert (
        results[0].headword
        == "Example"
    )


def test_cascade_uses_fuzzy():

    results = search_cascade(
        "exmple",
        ENTRIES
    )

    assert results

    assert (
        results[0].headword
        == "Example"
    )