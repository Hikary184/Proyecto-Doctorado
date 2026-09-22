from rapidfuzz.distance import (
    Levenshtein
)

from src.models.lexical_entry import (
    LexicalEntry
)

from src.normalization.normalizer import (
    normalize_form
)

from src.retrieval.models import (
    RetrievalResult
)


def search_fuzzy_normalized(
    query: str,
    entries: list[LexicalEntry],
    top_k: int = 5,
    threshold: float = 0.60
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

        if candidate is None:
            continue

        score = (
            Levenshtein
            .normalized_similarity(
                normalized_query,
                candidate
            )
        )

        if score >= threshold:

            results.append(
                RetrievalResult(
                    entry_id=entry.id,
                    headword=entry.headword,
                    normalized_form=candidate,
                    score=score,
                    method="fuzzy_normalized"
                )
            )

    results.sort(
        key=lambda result: result.score,
        reverse=True
    )

    return results[:top_k]