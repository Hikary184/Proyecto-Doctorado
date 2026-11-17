from collections import Counter

from src.models.lexical_entry import (
    LexicalEntry
)

from src.normalization.normalizer import (
    normalize_form
)


def build_quality_report(
    entries: list[LexicalEntry],
    rejected_count: int = 0
) -> dict:

    total = len(entries)

    missing_pos = 0
    missing_senses = 0
    with_examples = 0
    with_pronunciation = 0
    with_audio = 0

    normalized_headwords = []

    for entry in entries:

        if not entry.part_of_speech:
            missing_pos += 1

        if not entry.senses:
            missing_senses += 1

        if any(
            sense.examples
            for sense in entry.senses
        ):
            with_examples += 1

        if entry.pronunciations:
            with_pronunciation += 1

        if entry.audio:
            with_audio += 1

        normalized = normalize_form(
            entry.headword
        ).normalized_form

        normalized_headwords.append(
            normalized
        )

    frequencies = Counter(
        normalized_headwords
    )

    duplicate_candidates = {
        form: count
        for form, count in frequencies.items()
        if count > 1
    }

    return {
        "total_valid_entries": total,

        "rejected_entries":
            rejected_count,

        "missing_part_of_speech":
            missing_pos,

        "missing_senses":
            missing_senses,

        "entries_with_examples":
            with_examples,

        "entries_with_pronunciation":
            with_pronunciation,

        "entries_with_audio":
            with_audio,

        "duplicate_headword_candidates":
            duplicate_candidates
    }