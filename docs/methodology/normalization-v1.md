# Lexical Normalization — Version 1.0

## Purpose

The normalization module generates a computational
representation of lexical forms while preserving the
original source representation.

## Baseline operations

1. Unicode canonical normalization using NFC.
2. Removal of leading and trailing whitespace.
3. Collapse of repeated internal whitespace.
4. Unicode-aware case folding.

## Conservative principles

The baseline normalization does not:

- remove diacritics;
- replace phonological symbols;
- modify punctuation;
- merge orthographic variants;
- infer linguistic information.

Language-specific normalization rules are implemented
through explicit profiles and must be linguistically
motivated.

## Reproducibility

Each processed entry records:

- normalized form;
- method;
- version;
- normalization profile;
- operations applied.