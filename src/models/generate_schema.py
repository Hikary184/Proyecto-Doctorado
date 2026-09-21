import json
from pathlib import Path

from src.models.lexical_entry import LexicalEntry


OUTPUT = Path(
    "data/schemas/lexical_entry.schema.json"
)


def generate_schema():

    schema = LexicalEntry.model_json_schema()

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            schema,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Schema generated: {OUTPUT}"
    )


if __name__ == "__main__":
    generate_schema()