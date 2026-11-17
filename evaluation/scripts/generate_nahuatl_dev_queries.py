import json
import random
import unicodedata

from collections import defaultdict
from pathlib import Path


CORPUS_FILE = Path(
    "data/processed/nahuatl/"
    "nahuatl_entries.json"
)

OUTPUT_FILE = Path(
    "evaluation/gold/"
    "nahuatl_dev_queries_v0_1.json"
)

SEED = 42

QUERIES_PER_CATEGORY = 5


def remove_diacritics(text: str) -> str:

    decomposed = unicodedata.normalize(
        "NFD",
        text
    )

    return "".join(
        char
        for char in decomposed
        if not unicodedata.combining(char)
    )


def deletion_variant(word: str) -> str:

    position = len(word) // 2

    return (
        word[:position]
        +
        word[position + 1:]
    )


def insertion_variant(word: str) -> str:

    position = len(word) // 2

    return (
        word[:position]
        +
        word[position]
        +
        word[position:]
    )


def substitution_variant(
    word: str
) -> str:

    position = len(word) // 2

    original = word[position]

    replacement = (
        "x"
        if original.lower() != "x"
        else "k"
    )

    return (
        word[:position]
        +
        replacement
        +
        word[position + 1:]
    )


def transposition_variant(
    word: str
) -> str:

    position = (
        len(word) // 2
    )

    if position >= len(word) - 1:
        position -= 1

    characters = list(word)

    characters[position], characters[position + 1] = (
        characters[position + 1],
        characters[position]
    )

    return "".join(characters)


def main():

    random_generator = random.Random(
        SEED
    )

    # --------------------------------------------
    # Load processed corpus
    # --------------------------------------------

    with open(
        CORPUS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        entries = json.load(file)

    print()
    print("NAHUATL DEV QUERY GENERATOR")
    print("=" * 60)

    print(
        f"Corpus entries: {len(entries)}"
    )

    # --------------------------------------------
    # Group entries by canonical headword
    # --------------------------------------------

    groups = defaultdict(list)

    for entry in entries:

        groups[
            entry["headword"]
        ].append(entry)

    all_headwords = set(
        groups.keys()
    )

    unique_groups = {
        headword: values
        for headword, values
        in groups.items()
        if len(values) == 1
    }

    ambiguous_groups = {
        headword: values
        for headword, values
        in groups.items()
        if len(values) > 1
    }

    print(
        f"Canonical forms: "
        f"{len(groups)}"
    )

    print(
        f"Unique forms: "
        f"{len(unique_groups)}"
    )

    print(
        f"Ambiguous forms: "
        f"{len(ambiguous_groups)}"
    )

    queries = []

    used_headwords = set()

    # --------------------------------------------
    # Helper
    # --------------------------------------------

    def add_query(
        category,
        source_headword,
        query,
        relevant_entries,
        transformation
    ):

        query_number = (
            len(queries) + 1
        )

        queries.append({

            "query_id":
                f"nah-dev-{query_number:03d}",

            "query":
                query,

            "category":
                category,

            "source_headword":
                source_headword,

            "relevant_ids": [
                entry["id"]
                for entry
                in relevant_entries
            ],

            "transformation":
                transformation,

            "status":
                "auto_generated_needs_review"
        })

        used_headwords.add(
            source_headword
        )

    # --------------------------------------------
    # Select candidates
    # --------------------------------------------

    def select_candidates(
        candidates,
        category,
        transform_function,
        count=QUERIES_PER_CATEGORY
    ):

        candidates = list(
            candidates.items()
        )

        random_generator.shuffle(
            candidates
        )

        selected = 0

        for headword, values in candidates:

            if headword in used_headwords:
                continue

            query = transform_function(
                headword
            )

            if not query:
                continue

            if query == headword:
                continue

            # Avoid accidentally generating another
            # existing canonical headword.
            if (
                category not in {
                    "case",
                    "whitespace"
                }
                and
                query in all_headwords
            ):
                continue

            add_query(
                category=category,
                source_headword=headword,
                query=query,
                relevant_entries=values,
                transformation=category
            )

            selected += 1

            if selected >= count:
                break

        if selected < count:

            raise RuntimeError(
                f"Not enough candidates for "
                f"category '{category}'. "
                f"Selected {selected}/{count}."
            )

    # --------------------------------------------
    # Simple lexical candidates
    # --------------------------------------------

    simple_words = {
        headword: values
        for headword, values
        in unique_groups.items()
        if (
            len(headword) >= 5
            and
            headword.isalpha()
        )
    }

    # --------------------------------------------
    # EXACT
    # --------------------------------------------

    exact_candidates = list(
        simple_words.items()
    )

    random_generator.shuffle(
        exact_candidates
    )

    for headword, values in (
        exact_candidates[
            :QUERIES_PER_CATEGORY
        ]
    ):

        add_query(
            category="exact",
            source_headword=headword,
            query=headword,
            relevant_entries=values,
            transformation="none"
        )

    # --------------------------------------------
    # CASE
    # --------------------------------------------

    select_candidates(
        simple_words,
        "case",
        lambda value:
            value.upper()
    )

    # --------------------------------------------
    # WHITESPACE
    # --------------------------------------------

    select_candidates(
        simple_words,
        "whitespace",
        lambda value:
            f"  {value}  "
    )

    # --------------------------------------------
    # DELETION
    # --------------------------------------------

    select_candidates(
        simple_words,
        "deletion",
        deletion_variant
    )

    # --------------------------------------------
    # INSERTION
    # --------------------------------------------

    select_candidates(
        simple_words,
        "insertion",
        insertion_variant
    )

    # --------------------------------------------
    # SUBSTITUTION
    # --------------------------------------------

    select_candidates(
        simple_words,
        "substitution",
        substitution_variant
    )

    # --------------------------------------------
    # TRANSPOSITION
    # --------------------------------------------

    transposition_candidates = {
        headword: values
        for headword, values
        in simple_words.items()
        if len(headword) >= 6
    }

    select_candidates(
        transposition_candidates,
        "transposition",
        transposition_variant
    )

    # --------------------------------------------
    # DIACRITIC
    # --------------------------------------------

    diacritic_candidates = {
        headword: values
        for headword, values
        in unique_groups.items()
        if (
            remove_diacritics(
                headword
            )
            != headword
        )
    }

    select_candidates(
        diacritic_candidates,
        "diacritic",
        remove_diacritics
    )

    # --------------------------------------------
    # MULTIWORD
    # --------------------------------------------

    multiword_candidates = [
        (headword, values)
        for headword, values
        in unique_groups.items()
        if " " in headword
        and headword not in used_headwords
    ]

    random_generator.shuffle(
        multiword_candidates
    )

    if (
        len(multiword_candidates)
        <
        QUERIES_PER_CATEGORY
    ):

        raise RuntimeError(
            "Not enough multiword candidates."
        )

    for headword, values in (
        multiword_candidates[
            :QUERIES_PER_CATEGORY
        ]
    ):

        add_query(
            category="multiword",
            source_headword=headword,
            query=headword,
            relevant_entries=values,
            transformation="none"
        )

    # --------------------------------------------
    # AMBIGUITY
    # --------------------------------------------

    ambiguity_candidates = [
        (headword, values)
        for headword, values
        in ambiguous_groups.items()
        if (
            headword not in
            used_headwords
        )
    ]

    random_generator.shuffle(
        ambiguity_candidates
    )

    if (
        len(ambiguity_candidates)
        <
        QUERIES_PER_CATEGORY
    ):

        raise RuntimeError(
            "Not enough ambiguity candidates."
        )

    for headword, values in (
        ambiguity_candidates[
            :QUERIES_PER_CATEGORY
        ]
    ):

        add_query(
            category="ambiguity",
            source_headword=headword,
            query=headword,
            relevant_entries=values,
            transformation="none"
        )

    # --------------------------------------------
    # Save
    # --------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            queries,
            file,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------
    # Summary
    # --------------------------------------------

    category_counts = defaultdict(
        int
    )

    for query in queries:

        category_counts[
            query["category"]
        ] += 1

    print()
    print("QUERY DATASET")
    print("=" * 60)

    print(
        f"Total queries: "
        f"{len(queries)}"
    )

    for category in sorted(
        category_counts
    ):

        print(
            f"{category}: "
            f"{category_counts[category]}"
        )

    print()
    print(
        f"Output: {OUTPUT_FILE}"
    )

    print()
    print(
        "IMPORTANT: This is a development "
        "robustness set, not the final "
        "linguistic gold standard."
    )


if __name__ == "__main__":
    main()