from fastapi import FastAPI
from src.models.lexical_entry import LexicalEntry
from pydantic import BaseModel

from src.normalization.normalizer import (
    normalize_form
)

from src.retrieval.corpus import (
    load_corpus
)

from src.retrieval.exact import (
    search_exact_raw,
    search_exact_normalized
)

from src.retrieval.fuzzy import (
    search_fuzzy_normalized
)

CORPUS_PATH = (
    "data/processed/"
    "sample_entries.normalized.json"
)

ENTRIES = load_corpus(
    CORPUS_PATH
)

app = FastAPI(
    title="Indigenous Dictionary Retrieval API",
    description="Research API for linguistic information retrieval in Indigenous-language dictionaries.",
    version="0.1.0"
)




@app.get("/")
def root():
    return {
        "project": "Indigenous Dictionary Retrieval",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
    
@app.post("/api/v1/validate-entry")
def validate_entry(entry: LexicalEntry):

    return {
        "valid": True,
        "id": entry.id,
        "headword": entry.headword,
        "language": entry.language.name
    }
    
class NormalizeRequest(BaseModel):
    text: str


@app.post("/api/v1/normalize")
def normalize(
    request: NormalizeRequest
):

    result = normalize_form(
        request.text
    )
    


@app.get("/api/v1/search/raw")
def search_raw(
    q: str
):

    return search_exact_raw(
        q,
        ENTRIES
    )


@app.get("/api/v1/search/normalized")
def search_normalized(
    q: str
):

    return search_exact_normalized(
        q,
        ENTRIES
    )


@app.get("/api/v1/search/fuzzy")
def search_fuzzy(
    q: str,
    top_k: int = 5,
    threshold: float = 0.60
):

    return search_fuzzy_normalized(
        q,
        ENTRIES,
        top_k=top_k,
        threshold=threshold
    )