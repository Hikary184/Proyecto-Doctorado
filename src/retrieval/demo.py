from src.retrieval.corpus import (
    load_corpus
)

from src.retrieval.exact import (
    search_exact_raw,
    search_exact_normalized
)

from src.retrieval.fuzzy import (
    search_fuzzy_normalized
)


CORPUS = (
    "data/processed/"
    "sample_entries.normalized.json"
)


entries = load_corpus(
    CORPUS
)


queries = [
    "Example",
    "example",
    "EXAMPLE",
    " exAmple ",
    "exampel",
    "exmple",
    "csa",
    "ÁRBOL",
    "árbol",
    "arbol"
]


for query in queries:

    print()
    print("=" * 60)

    print(
        f"QUERY: {repr(query)}"
    )

    print("=" * 60)

    # --------------------------------------
    # B0
    # --------------------------------------

    raw_results = search_exact_raw(
        query,
        entries
    )

    print()
    print("B0 - EXACT RAW")

    if not raw_results:

        print("No results")

    for result in raw_results:

        print(
            result.model_dump()
        )

    # --------------------------------------
    # B1
    # --------------------------------------

    normalized_results = (
        search_exact_normalized(
            query,
            entries
        )
    )

    print()
    print("B1 - EXACT NORMALIZED")

    if not normalized_results:

        print("No results")

    for result in normalized_results:

        print(
            result.model_dump()
        )

    # --------------------------------------
    # B2
    # --------------------------------------

    fuzzy_results = (
        search_fuzzy_normalized(
            query,
            entries,
            top_k=3
        )
    )

    print()
    print("B2 - FUZZY NORMALIZED")

    if not fuzzy_results:

        print("No results")

    for result in fuzzy_results:

        print(
            result.model_dump()
        )