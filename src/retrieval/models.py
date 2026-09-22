from pydantic import BaseModel


class RetrievalResult(BaseModel):

    entry_id: str

    headword: str

    normalized_form: str | None = None

    score: float

    method: str