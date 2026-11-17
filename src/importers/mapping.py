from src.importers.ids import (
    create_entry_id
)

from src.importers.models import (
    RawLexicalRecord
)

from src.models.lexical_entry import (
    LexicalEntry,
    LanguageInfo,
    Variant,
    Pronunciation,
    Example,
    Sense,
    Metadata
)


def map_raw_record(
    record: RawLexicalRecord,
    language_name: str,
    language_key: str,
    iso639_3: str | None = None,
    glottocode: str | None = None,
    variety: str | None = None,
    source_name: str | None = None
) -> LexicalEntry:

    if not record.headword:

        raise ValueError(
            "Record has no headword."
        )

    entry_id = create_entry_id(
        language_key=language_key,
        source_index=record.source_index,
        source_id=record.source_id
    )

    variants = [
        Variant(
            form=form
        )
        for form in record.variants
        if form
    ]

    pronunciations = [
        Pronunciation(
            transcription=value
        )
        for value in record.pronunciations
        if value
    ]

    examples = [
        Example(
            text=text
        )
        for text in record.examples
        if text
    ]

    senses = []

    has_sense_information = any([
        record.definition,
        record.gloss_es,
        record.gloss_en,
        examples
    ])

    if has_sense_information:

        senses.append(
            Sense(
                id=f"{entry_id}-sense-1",

                definition=record.definition,

                gloss_es=record.gloss_es,

                gloss_en=record.gloss_en,

                examples=examples
            )
        )

    return LexicalEntry(
        id=entry_id,

        language=LanguageInfo(
            name=language_name,
            iso639_3=iso639_3,
            glottocode=glottocode,
            variety=variety
        ),

        headword=record.headword,

        part_of_speech=(
            record.part_of_speech
        ),

        variants=variants,

        pronunciations=pronunciations,

        senses=senses,

        metadata=Metadata(
            source=source_name,
            source_entry_id=record.source_id
        )
    )