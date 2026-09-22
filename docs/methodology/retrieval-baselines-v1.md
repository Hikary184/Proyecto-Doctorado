# Retrieval Baselines — Version 1.0

## B0 — Exact Raw

Direct string comparison between the user query
and the original lexical headword.

No preprocessing is applied.

## B1 — Exact Normalized

Both lexical entries and queries are transformed
using the lexical normalization pipeline.

Exact comparison is subsequently performed.

## B2 — Fuzzy Normalized

Queries and lexical entries are normalized before
comparison.

Similarity is calculated using normalized
Levenshtein similarity.

Results are ranked in descending order according
to similarity score.

## Parameters

Default threshold:

0.60

Default Top-K:

5

These values are preliminary and will be evaluated
experimentally.