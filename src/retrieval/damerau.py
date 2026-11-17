from rapidfuzz.distance import (
    DamerauLevenshtein
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


def search_damerau_normalized(
    query: str,
    entries: list[LexicalEntry],
    top_k: int = 5,
    threshold: float = 0.60
) -> list[RetrievalResult]:

    normalized_query = (
        normalize_form(query)
        .normalized_form
    )

    results = []

    for entry in entries:

        normalization = (
            entry
            .computational_analysis
            .normalization
        )

        if normalization is None:
            continue

        normalized_entry = (
            normalization.normalized_form
        )

        if normalized_entry is None:
            continue

        score = (
            DamerauLevenshtein
            .normalized_similarity(
                normalized_query,
                normalized_entry
            )
        )

        if score >= threshold:

            results.append(
                RetrievalResult(
                    entry_id=entry.id,
                    headword=entry.headword,
                    normalized_form=(
                        normalized_entry
                    ),
                    score=score,
                    method=(
                        "damerau_normalized"
                    )
                )
            )

    results.sort(
        key=lambda item:
            item.score,
        reverse=True
    )

    return results[:top_k]