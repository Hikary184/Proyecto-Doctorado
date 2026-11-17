import json
import re
import unicodedata

from collections import Counter
from pathlib import Path

from src.importers.parsers.nahuatl_txt import (
    parse_nahuatl_txt
)


SOURCE_FILE = Path(
    "data/raw/nahuatl/source/nau-es.txt"
)

OUTPUT_FILE = Path(
    "results/import_reports/"
    "nahuatl_corpus_statistics.json"
)


def normalize_for_analysis(
    text: str
) -> str:

    text = unicodedata.normalize(
        "NFC",
        text
    )

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.casefold()


def main():

    records, rejected = (
        parse_nahuatl_txt(
            SOURCE_FILE
        )
    )

    source_headwords = [
        record.extra.get(
            "source_headword",
            record.headword
        )
        for record in records
    ]

    canonical_headwords = [
        record.headword
        for record in records
    ]

    normalized_headwords = [
        normalize_for_analysis(
            headword
        )
        for headword
        in canonical_headwords
    ]

    numbered_senses = [
        record
        for record in records
        if (
            record.extra.get(
                "sense_number"
            )
            is not None
        )
    ]

    multiword_entries = [
        headword
        for headword
        in canonical_headwords
        if len(
            headword.split()
        ) > 1
    ]

    prefixes = [
        headword
        for headword
        in canonical_headwords
        if headword.endswith("-")
    ]

    questions = [
        headword
        for headword
        in canonical_headwords
        if (
            "?" in headword
            or
            "¿" in headword
        )
    ]

    exclamations = [
        headword
        for headword
        in canonical_headwords
        if (
            "!" in headword
            or
            "¡" in headword
        )
    ]

    raw_frequencies = Counter(
        source_headwords
    )

    canonical_frequencies = Counter(
        canonical_headwords
    )

    normalized_frequencies = Counter(
        normalized_headwords
    )

    exact_duplicate_groups = {
        form: count
        for form, count
        in raw_frequencies.items()
        if count > 1
    }

    canonical_collision_groups = {
        form: count
        for form, count
        in canonical_frequencies.items()
        if count > 1
    }

    normalized_collision_groups = {
        form: count
        for form, count
        in normalized_frequencies.items()
        if count > 1
    }

    report = {

        "total_records":
            len(records),

        "rejected_records":
            len(rejected),

        "unique_source_headwords":
            len(set(source_headwords)),

        "unique_canonical_headwords":
            len(set(canonical_headwords)),

        "unique_normalized_headwords":
            len(set(normalized_headwords)),

        "numbered_sense_entries":
            len(numbered_senses),

        "multiword_entries":
            len(multiword_entries),

        "prefix_entries":
            len(prefixes),

        "question_entries":
            len(questions),

        "exclamation_entries":
            len(exclamations),

        "exact_duplicate_groups":
            len(exact_duplicate_groups),

        "canonical_collision_groups":
            len(
                canonical_collision_groups
            ),

        "normalized_collision_groups":
            len(
                normalized_collision_groups
            ),

        "normalized_collisions":
            normalized_collision_groups
    }

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
            report,
            file,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("NAHUATL CORPUS STATISTICS")
    print("=" * 60)

    for key, value in report.items():

        if key == "normalized_collisions":
            continue

        print(
            f"{key}: {value}"
        )

    print()
    print(
        f"Report saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()