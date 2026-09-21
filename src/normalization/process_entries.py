import json

from pathlib import Path

from src.models.lexical_entry import (
    LexicalEntry
)

from src.normalization.normalizer import (
    normalize_form
)

from src.normalization.profiles import (
    get_profile
)


INPUT_FILE = Path(
    "data/samples/sample_entries.json"
)

OUTPUT_FILE = Path(
    "data/processed/sample_entries.normalized.json"
)


def process_entries():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        raw_data = json.load(file)

    processed_entries = []

    for raw_entry in raw_data:

        entry = LexicalEntry.model_validate(
            raw_entry
        )

        language_code = (
            entry.language.iso639_3
        )

        profile = get_profile(
            language_code
        )

        analysis = normalize_form(
            entry.headword,
            profile
        )

        entry.computational_analysis.normalization = (
            analysis
        )

        processed_entries.append(
            entry.model_dump(
                mode="json"
            )
        )

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
            processed_entries,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Processed entries: {len(processed_entries)}"
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    process_entries()