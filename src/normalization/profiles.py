from typing import Dict, Literal

from pydantic import BaseModel, Field


class NormalizationProfile(BaseModel):

    name: str

    unicode_form: Literal[
        "NFC",
        "NFD",
        "NFKC",
        "NFKD"
    ] = "NFC"

    strip_whitespace: bool = True

    collapse_whitespace: bool = True

    casefold: bool = True

    replacements: Dict[str, str] = Field(
        default_factory=dict
    )


GENERIC_SEARCH_PROFILE = NormalizationProfile(

    name="generic_search",

    unicode_form="NFC",

    strip_whitespace=True,

    collapse_whitespace=True,

    casefold=True,

    replacements={}
)

LANGUAGE_PROFILES = {

    "default": GENERIC_SEARCH_PROFILE

}


def get_profile(
    language_code: str | None
) -> NormalizationProfile:

    if language_code is None:

        return GENERIC_SEARCH_PROFILE

    return LANGUAGE_PROFILES.get(
        language_code,
        GENERIC_SEARCH_PROFILE
    )