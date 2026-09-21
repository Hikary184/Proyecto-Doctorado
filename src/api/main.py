from fastapi import FastAPI
from src.models.lexical_entry import LexicalEntry
from pydantic import BaseModel

from src.normalization.normalizer import (
    normalize_form
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