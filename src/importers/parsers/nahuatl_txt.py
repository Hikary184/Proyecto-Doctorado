import re

from pathlib import Path

from src.importers.models import (
    RawLexicalRecord
)


SENSE_PATTERN = re.compile(
    r"^(.*?)\s+(\d+)$"
)


def parse_headword(
    source_headword: str
) -> tuple[str, int | None]:

    source_headword = (
        source_headword.strip()
    )

    match = SENSE_PATTERN.match(
        source_headword
    )

    if match:

        headword = (
            match.group(1).strip()
        )

        sense_number = int(
            match.group(2)
        )

        return (
            headword,
            sense_number
        )

    return (
        source_headword,
        None
    )


def parse_nahuatl_txt(
    file_path: str | Path,
    limit: int | None = None
) -> tuple[
    list[RawLexicalRecord],
    list[dict]
]:

    path = Path(file_path)

    records = []
    rejected = []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
        ):

            line = line.rstrip(
                "\n\r"
            )

            if not line.strip():
                continue

            if ":" not in line:

                rejected.append({
                    "line": line_number,
                    "reason": "missing_colon",
                    "raw_text": line
                })

                continue

            source_headword, spanish_text = (
                line.split(
                    ":",
                    maxsplit=1
                )
            )

            source_headword = (
                source_headword.strip()
            )

            spanish_text = (
                spanish_text.strip()
            )

            if not source_headword:

                rejected.append({
                    "line": line_number,
                    "reason": "missing_headword",
                    "raw_text": line
                })

                continue

            if not spanish_text:

                rejected.append({
                    "line": line_number,
                    "reason": "missing_spanish_text",
                    "raw_text": line
                })

                continue

            headword, sense_number = (
                parse_headword(
                    source_headword
                )
            )

            record = RawLexicalRecord(
                source_index=line_number,

                source_id=(
                    f"line-{line_number}"
                ),

                headword=headword,

                gloss_es=spanish_text,

                raw_text=line,

                extra={
                    "source_headword":
                        source_headword,

                    "sense_number":
                        sense_number
                }
            )

            records.append(
                record
            )

            if (
                limit is not None
                and
                len(records) >= limit
            ):
                break

    return records, rejected