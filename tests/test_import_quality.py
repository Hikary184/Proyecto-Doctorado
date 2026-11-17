from src.importers.mapping import (
    map_raw_record
)

from src.importers.models import (
    RawLexicalRecord
)

from src.importers.quality import (
    build_quality_report
)


def test_quality_report():

    raw_records = [

        RawLexicalRecord(
            source_index=1,
            headword="aaki",
            gloss_es="gozar"
        ),

        RawLexicalRecord(
            source_index=2,
            headword="aaki",
            gloss_es="hundir"
        ),

        RawLexicalRecord(
            source_index=3,
            headword="aakatl",
            gloss_es="caña de río"
        )
    ]

    entries = [

        map_raw_record(
            record,
            language_name="Náhuatl",
            language_key="nahuatl"
        )

        for record in raw_records
    ]

    report = build_quality_report(
        entries
    )

    assert (
        report["total_valid_entries"]
        == 3
    )

    assert (
        report["missing_part_of_speech"]
        == 3
    )

    assert (
        report["missing_senses"]
        == 0
    )

    assert (
        report[
            "duplicate_headword_candidates"
        ]["aaki"]
        == 2
    )