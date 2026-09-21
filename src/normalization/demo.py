from src.normalization.normalizer import (
    normalize_form
)


examples = [

    "  EXAMPLE  ",

    "Example",

    "EXAMPLE",

    "  example    word ",

    "ÁRBOL",

    "a\u0301"
]


for form in examples:

    result = normalize_form(form)

    print("----------------------------")

    print(
        f"Original:   {repr(form)}"
    )

    print(
        f"Normalized: {repr(result.normalized_form)}"
    )

    print(
        f"Operations: {result.operations}"
    )