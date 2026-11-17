from src.models.lexical_entry import (
    LexicalEntry
)

from src.retrieval.models import (
    RetrievalResult
)

from src.retrieval.exact import (
    search_exact_raw,
    search_exact_normalized
)

from src.retrieval.damerau import (
    search_damerau_normalized
)


def search_cascade_damerau(
    query: str,
    entries: list[LexicalEntry],
    top_k: int = 5,
    threshold: float = 0.60
) -> list[RetrievalResult]:

    # --------------------------------------------------
    # Stage 1: Exact raw
    # --------------------------------------------------

    raw_results = search_exact_raw(
        query,
        entries
    )

    if raw_results:

        return raw_results[:top_k]

    # --------------------------------------------------
    # Stage 2: Exact normalized
    # --------------------------------------------------

    normalized_results = (
        search_exact_normalized(
            query,
            entries
        )
    )

    if normalized_results:

        return normalized_results[:top_k]

    # --------------------------------------------------
    # Stage 3: Damerau-Levenshtein
    # --------------------------------------------------

    return search_damerau_normalized(
        query,
        entries,
        top_k=top_k,
        threshold=threshold
    )