import json
from pathlib import Path
from pydantic import ValidationError

from src.models.lexical_entry import LexicalEntry


DATA_FILE = Path("data/samples/sample_entries.json")


def validate_entries():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    valid_entries = 0
    invalid_entries = 0

    for raw_entry in data:

        try:

            entry = LexicalEntry.model_validate(raw_entry)

            print(
                f"[VALID] {entry.id}: {entry.headword}"
            )

            valid_entries += 1

        except ValidationError as error:

            print(
                f"[INVALID] Entry: {raw_entry.get('id')}"
            )

            print(error)

            invalid_entries += 1

    print()
    print("Validation finished")
    print("-------------------")
    print(f"Valid entries:   {valid_entries}")
    print(f"Invalid entries: {invalid_entries}")


if __name__ == "__main__":
    validate_entries()