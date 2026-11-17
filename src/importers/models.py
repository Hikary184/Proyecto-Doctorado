from typing import Any

from pydantic import BaseModel, Field


class RawLexicalRecord(BaseModel):
    source_index: int

    source_id: str | None = None

    headword: str | None = None

    part_of_speech: str | None = None

    definition: str | None = None

    gloss_es: str | None = None

    gloss_en: str | None = None

    variants: list[str] = Field(
        default_factory=list
    )

    pronunciations: list[str] = Field(
        default_factory=list
    )

    examples: list[str] = Field(
        default_factory=list
    )

    audio_files: list[str] = Field(
        default_factory=list
    )

    raw_text: str | None = None

    extra: dict[str, Any] = Field(
        default_factory=dict
    )