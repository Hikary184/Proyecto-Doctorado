from pydantic import BaseModel
from typing import Optional, List


class LexicalEntry(BaseModel):
    id: str
    language: str
    headword: str

    part_of_speech: Optional[str] = None
    definition: Optional[str] = None

    variants: List[str] = []
    pronunciations: List[str] = []