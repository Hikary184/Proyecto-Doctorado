import re
import unicodedata

from src.models.lexical_entry import NormalizationAnalysis

from src.normalization.profiles import (
    NormalizationProfile,
    GENERIC_SEARCH_PROFILE
)


NORMALIZER_VERSION = "1.0"


def normalize_form(
    text: str,
    profile: NormalizationProfile = GENERIC_SEARCH_PROFILE
) -> NormalizationAnalysis:

    if not isinstance(text, str):
        raise TypeError(
            "The form to normalize must be a string."
        )

    value = text

    operations = []

    # --------------------------------------------------
    # Unicode normalization
    # --------------------------------------------------

    normalized_unicode = unicodedata.normalize(
        profile.unicode_form,
        value
    )

    if normalized_unicode != value:
        operations.append(
            f"unicode:{profile.unicode_form}"
        )

    value = normalized_unicode

    # --------------------------------------------------
    # Language/profile-specific replacements
    # --------------------------------------------------

    for source, target in profile.replacements.items():

        if source in value:

            value = value.replace(
                source,
                target
            )

            operations.append(
                f"replace:{source}->{target}"
            )

    # --------------------------------------------------
    # Leading/trailing whitespace
    # --------------------------------------------------

    if profile.strip_whitespace:

        stripped = value.strip()

        if stripped != value:
            operations.append(
                "strip_whitespace"
            )

        value = stripped

    # --------------------------------------------------
    # Internal whitespace
    # --------------------------------------------------

    if profile.collapse_whitespace:

        collapsed = re.sub(
            r"\s+",
            " ",
            value
        )

        if collapsed != value:
            operations.append(
                "collapse_whitespace"
            )

        value = collapsed

    # --------------------------------------------------
    # Unicode-aware lowercase normalization
    # --------------------------------------------------

    if profile.casefold:

        casefolded = value.casefold()

        if casefolded != value:
            operations.append(
                "casefold"
            )

        value = casefolded

    return NormalizationAnalysis(

        normalized_form=value,

        method="unicode_normalizer",

        version=NORMALIZER_VERSION,

        profile=profile.name,

        operations=operations
    )