from typing import Optional, List
from pydantic import BaseModel, Field


# ============================================================
# LANGUAGE
# ============================================================

class LanguageInfo(BaseModel):
    name: str
    iso639_3: Optional[str] = None
    glottocode: Optional[str] = None
    variety: Optional[str] = None


# ============================================================
# VARIANTS
# ============================================================

class Variant(BaseModel):
    form: str
    type: Optional[str] = None
    variety: Optional[str] = None
    notes: Optional[str] = None


# ============================================================
# PRONUNCIATION
# ============================================================

class Pronunciation(BaseModel):
    transcription: str
    system: Optional[str] = None
    variety: Optional[str] = None
    audio_id: Optional[str] = None


# ============================================================
# EXAMPLES
# ============================================================

class Example(BaseModel):
    text: str

    translation_es: Optional[str] = None
    translation_en: Optional[str] = None

    source: Optional[str] = None
    audio_id: Optional[str] = None


# ============================================================
# SENSES
# ============================================================

class Sense(BaseModel):
    id: str

    definition: Optional[str] = None

    gloss_es: Optional[str] = None
    gloss_en: Optional[str] = None

    semantic_domain: Optional[str] = None

    examples: List[Example] = Field(default_factory=list)


# ============================================================
# AUDIO
# ============================================================

class AudioFile(BaseModel):
    id: str

    file_name: str

    speaker_id: Optional[str] = None
    variety: Optional[str] = None

    duration: Optional[float] = None
    format: Optional[str] = None

    license: Optional[str] = None


# ============================================================
# METADATA
# ============================================================

class Metadata(BaseModel):
    source: Optional[str] = None
    source_entry_id: Optional[str] = None

    annotator: Optional[str] = None
    validator: Optional[str] = None

    date_created: Optional[str] = None
    date_modified: Optional[str] = None

    validation_status: Optional[str] = None

    notes: Optional[str] = None


# ============================================================
# COMPUTATIONAL NORMALIZATION
# ============================================================

class NormalizationAnalysis(BaseModel):
    normalized_form: Optional[str] = None

    method: Optional[str] = None
    version: Optional[str] = None

    profile: Optional[str] = None

    operations: List[str] = Field(
        default_factory=list
    )


# ============================================================
# MORPHOLOGY
# ============================================================

class Morpheme(BaseModel):
    form: str

    type: Optional[str] = None
    gloss: Optional[str] = None


class MorphologicalAnalysis(BaseModel):
    base: Optional[str] = None
    root: Optional[str] = None

    morphemes: List[Morpheme] = Field(default_factory=list)

    method: Optional[str] = None
    model: Optional[str] = None

    confidence: Optional[float] = None


# ============================================================
# PHONOLOGY
# ============================================================

class PhonologicalAnalysis(BaseModel):
    ipa: Optional[str] = None

    normalized_ipa: Optional[str] = None

    method: Optional[str] = None
    model: Optional[str] = None

    confidence: Optional[float] = None


# ============================================================
# SEMANTIC INFORMATION
# ============================================================

class SemanticAnalysis(BaseModel):
    model: Optional[str] = None

    embedding_id: Optional[str] = None

    semantic_tags: List[str] = Field(default_factory=list)


# ============================================================
# COMPUTATIONAL ANALYSIS
# ============================================================

class ComputationalAnalysis(BaseModel):

    normalization: Optional[NormalizationAnalysis] = None

    morphology: List[MorphologicalAnalysis] = Field(
        default_factory=list
    )

    phonology: List[PhonologicalAnalysis] = Field(
        default_factory=list
    )

    semantics: Optional[SemanticAnalysis] = None


# ============================================================
# MAIN LEXICAL ENTRY
# ============================================================

class LexicalEntry(BaseModel):

    id: str

    language: LanguageInfo

    headword: str

    part_of_speech: Optional[str] = None

    variants: List[Variant] = Field(default_factory=list)

    pronunciations: List[Pronunciation] = Field(
        default_factory=list
    )

    senses: List[Sense] = Field(default_factory=list)

    audio: List[AudioFile] = Field(default_factory=list)

    metadata: Metadata = Field(
        default_factory=Metadata
    )

    computational_analysis: ComputationalAnalysis = Field(
        default_factory=ComputationalAnalysis
    )