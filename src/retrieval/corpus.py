import json

from pathlib import Path

from src.models.lexical_entry import LexicalEntry


def load_corpus(
    file_path: str | Path
) -> list[LexicalEntry]:

    path = Path(file_path)

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        raw_data = json.load(file)

    entries = []

    for raw_entry in raw_data:

        entry = LexicalEntry.model_validate(
            raw_entry
        )

        entries.append(entry)

    return entries