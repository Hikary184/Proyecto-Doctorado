import json

from pathlib import Path

from src.importers.parsers.nahuatl_txt import (
    parse_nahuatl_txt
)

from src.importers.mapping import (
    map_raw_record
)

from src.importers.quality import (
    build_quality_report
)

from src.normalization.normalizer import (
    normalize_form
)


SOURCE_FILE = Path(
    "data/raw/nahuatl/source/nau-es.txt"
)

OUTPUT_DIR = Path(
    "data/processed/nahuatl"
)

REPORT_DIR = Path(
    "results/import_reports"
)


def main():

    print()
    print("NAHUATL CORPUS IMPORT")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Parse raw source
    # --------------------------------------------------

    raw_records, rejected = (
        parse_nahuatl_txt(
            SOURCE_FILE
        )
    )
        # --------------------------------------------------
    # Save intermediate representation
    # --------------------------------------------------

    intermediate_dir = Path(
        "data/intermediate/nahuatl"
    )

    intermediate_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    intermediate_file = (
        intermediate_dir
        /
        "nahuatl_raw_records.json"
    )

    with open(
        intermediate_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [
                record.model_dump(
                    mode="json"
                )
                for record
                in raw_records
            ],
            file,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Intermediate records: "
        f"{intermediate_file}"
    )

    print(
        f"Source records parsed: "
        f"{len(raw_records)}"
    )

    print(
        f"Rejected records: "
        f"{len(rejected)}"
    )

    # --------------------------------------------------
    # 2. Convert to LexicalEntry
    # --------------------------------------------------

    entries = []

    mapping_errors = []

    for record in raw_records:

        try:

            entry = map_raw_record(
                record=record,
                language_name="Náhuatl",
                language_key="nahuatl",
                source_name="nau-es.txt"
            )

            # ------------------------------------------
            # 3. Normalize headword
            # ------------------------------------------

            normalization = normalize_form(
                entry.headword
            )

            entry.computational_analysis.normalization = (
                normalization
            )

            entries.append(
                entry
            )

        except Exception as error:

            mapping_errors.append({
                "source_index":
                    record.source_index,

                "source_id":
                    record.source_id,

                "headword":
                    record.headword,

                "error":
                    str(error)
            })

    print(
        f"Valid lexical entries: "
        f"{len(entries)}"
    )

    print(
        f"Mapping errors: "
        f"{len(mapping_errors)}"
    )

    # --------------------------------------------------
    # 4. Quality report
    # --------------------------------------------------

    quality_report = build_quality_report(
        entries=entries,
        rejected_count=(
            len(rejected)
            +
            len(mapping_errors)
        )
    )

    report = {
        "language": "Náhuatl",

        "source_file":
            str(SOURCE_FILE),

        "records_parsed":
            len(raw_records),

        "valid_entries":
            len(entries),

        "parser_rejections":
            len(rejected),

        "mapping_errors":
            len(mapping_errors),

        "quality":
            quality_report
    }

    # --------------------------------------------------
    # 5. Create output directories
    # --------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # 6. Save processed corpus
    # --------------------------------------------------

    corpus_file = (
        OUTPUT_DIR
        /
        "nahuatl_entries.json"
    )

    with open(
        corpus_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [
                entry.model_dump(
                    mode="json"
                )
                for entry
                in entries
            ],
            file,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------------
    # 7. Save report
    # --------------------------------------------------

    report_file = (
        REPORT_DIR
        /
        "nahuatl_import_report.json"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------------
    # 8. Save rejected records
    # --------------------------------------------------

    rejected_file = (
        REPORT_DIR
        /
        "nahuatl_rejected.json"
    )

    with open(
        rejected_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "parser_rejections":
                    rejected,

                "mapping_errors":
                    mapping_errors
            },
            file,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------------
    # 9. Summary
    # --------------------------------------------------

    print()
    print("IMPORT SUMMARY")
    print("=" * 60)

    print(
        f"Processed corpus: "
        f"{corpus_file}"
    )

    print(
        f"Quality report: "
        f"{report_file}"
    )

    print(
        f"Rejected records: "
        f"{rejected_file}"
    )

    print()
    print("QUALITY")
    print("=" * 60)

    for key, value in (
        quality_report.items()
    ):

        if (
            key
            ==
            "duplicate_headword_candidates"
        ):

            print(
                f"{key}: "
                f"{len(value)} groups"
            )

        else:

            print(
                f"{key}: {value}"
            )


if __name__ == "__main__":
    main()