import pytest

from src.importers.mapping import (
    map_raw_record
)

from src.importers.models import (
    RawLexicalRecord
)


def test_mapping_minimal_record():

    raw = RawLexicalRecord(
        source_index=1,
        headword="aakatl",
        gloss_es="caña de río"
    )

    entry = map_raw_record(
        raw,
        language_name="Náhuatl",
        language_key="nahuatl"
    )

    assert entry.headword == "aakatl"
    assert entry.language.name == "Náhuatl"
    assert entry.id.startswith("nahuatl-")
    assert len(entry.senses) == 1
    assert entry.senses[0].gloss_es == "caña de río"


def test_mapping_numbered_sense():

    raw = RawLexicalRecord(
        source_index=10,
        source_id="line-10",
        headword="aaki",
        gloss_es="gozar",
        extra={
            "source_headword": "aaki 1",
            "sense_number": 1
        }
    )

    entry = map_raw_record(
        raw,
        language_name="Náhuatl",
        language_key="nahuatl",
        source_name="nau-es.txt"
    )

    assert entry.headword == "aaki"
    assert entry.metadata.source == "nau-es.txt"
    assert entry.metadata.source_entry_id == "line-10"


def test_mapping_requires_headword():

    raw = RawLexicalRecord(
        source_index=3
    )

    with pytest.raises(ValueError):

        map_raw_record(
            raw,
            language_name="Náhuatl",
            language_key="nahuatl"
        )