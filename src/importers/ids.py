import hashlib


def create_entry_id(
    language_key: str,
    source_index: int,
    source_id: str | None = None
) -> str:

    source_reference = (
        source_id
        if source_id
        else str(source_index)
    )

    raw_value = (
        f"{language_key}:"
        f"{source_reference}"
    )

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()[:12]

    return (
        f"{language_key}-"
        f"{digest}"
    )