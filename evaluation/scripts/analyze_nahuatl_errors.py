import csv
from pathlib import Path


INPUT_FILE = Path(
    "results/tables/"
    "nahuatl_dev_detailed.csv"
)

OUTPUT_FILE = Path(
    "results/tables/"
    "nahuatl_dev_errors.csv"
)


def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig"
    ) as file:

        rows = list(
            csv.DictReader(file)
        )

    errors = [
        row
        for row in rows
        if (
            row["method"]
            == "B2_fuzzy_normalized"
            and
            float(
                row["top1_accuracy"]
            )
            == 0.0
        )
    ]

    print()
    print("B2 NAHUATL ERROR ANALYSIS")
    print("=" * 72)

    print(
        f"Top-1 errors: {len(errors)}"
    )

    print()

    for row in errors:

        retrieved = (
            row["retrieved_ids"]
            .split("|")
        )

        relevant = (
            row["relevant_ids"]
            .split("|")
        )

        relevant_rank = None

        for index, entry_id in enumerate(
            retrieved,
            start=1
        ):

            if entry_id in relevant:

                relevant_rank = index
                break

        print("-" * 72)

        print(
            f"Query ID:       "
            f"{row['query_id']}"
        )

        print(
            f"Category:       "
            f"{row['category']}"
        )

        print(
            f"Query:          "
            f"{repr(row['query'])}"
        )

        print(
            f"Expected form:  "
            f"{row['source_headword']}"
        )

        print(
            f"Top result:     "
            f"{row['top_result_headword']}"
        )

        print(
            f"Top score:      "
            f"{row['top_result_score']}"
        )

        print(
            f"Relevant rank:  "
            f"{relevant_rank}"
        )

        print(
            f"Relevant IDs:   "
            f"{row['relevant_ids']}"
        )

        print(
            f"Retrieved IDs:  "
            f"{row['retrieved_ids']}"
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if errors:

        with open(
            OUTPUT_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=errors[0].keys()
            )

            writer.writeheader()

            writer.writerows(
                errors
            )

    print()
    print("=" * 72)

    print(
        f"Error report: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()