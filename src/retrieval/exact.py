from src.models.lexical_entry import LexicalEntry

from src.normalization.normalizer import (
    normalize_form
)

from src.retrieval.models import (
    RetrievalResult
)


# ============================================================
# B0 - EXACT RAW
# ============================================================

def search_exact_raw(
    query: str,
    entries: list[LexicalEntry]
) -> list[RetrievalResult]:

    results = []

    for entry in entries:

        if query == entry.headword:

            results.append(
                RetrievalResult(
                    entry_id=entry.id,
                    headword=entry.headword,
                    normalized_form=None,
                    score=1.0,
                    method="exact_raw"
                )
            )

    return results


# ============================================================
# B1 - EXACT NORMALIZED
# ============================================================

def search_exact_normalized(
    query: str,
    entries: list[LexicalEntry]
) -> list[RetrievalResult]:

    normalized_query = normalize_form(
        query
    ).normalized_form

    results = []

    for entry in entries:

        analysis = (
            entry
            .computational_analysis
            .normalization
        )

        if analysis is None:
            continue

        candidate = (
            analysis.normalized_form
        )

        if candidate == normalized_query:

            results.append(
                RetrievalResult(
                    entry_id=entry.id,
                    headword=entry.headword,
                    normalized_form=candidate,
                    score=1.0,
                    method="exact_normalized"
                )
            )

    return results