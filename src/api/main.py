from fastapi import FastAPI

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