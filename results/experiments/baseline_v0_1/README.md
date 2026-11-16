# Baseline Retrieval Experiment v0.1

## Purpose

Verify the experimental retrieval framework and compare
three basic lexical retrieval strategies.

This experiment uses synthetic development data and is not
intended to provide conclusions about real Indigenous
language retrieval performance.

## Methods

### B0 — Exact Raw

Direct comparison between the query and the original
headword.

### B1 — Exact Normalized

Exact comparison after Unicode NFC normalization,
whitespace normalization, and Unicode-aware case folding.

### B2 — Fuzzy Normalized

Normalized Levenshtein similarity applied after lexical
normalization.

Threshold: 0.60

Top-K: 5

## Dataset

Synthetic lexical corpus:

5 lexical entries.

Evaluation queries:

10 queries.

## Results

| Method | Top-1 | P@1 | P@5 | R@5 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|---:|---:|
| B0 Exact Raw | 0.10 | 0.10 | 0.02 | 0.10 | 0.10 | 0.10 |
| B1 Exact Normalized | 0.60 | 0.60 | 0.12 | 0.60 | 0.60 | 0.60 |
| B2 Fuzzy Normalized | 1.00 | 1.00 | 0.20 | 1.00 | 1.00 | 1.00 |

## Interpretation

Lexical normalization substantially increased retrieval
coverage for queries affected by capitalization and
whitespace variation.

Fuzzy retrieval additionally recovered forms affected by
deletion, character transposition, and missing diacritics.

The perfect B2 result should not be interpreted as evidence
of general retrieval performance because the experiment
uses a very small synthetic development set.

## Limitations

- Synthetic corpus.
- Only five lexical entries.
- Only ten queries.
- One relevant entry per query.
- No linguistic variation.
- No morphological phenomena.
- No phonological variation.
- No semantic retrieval.
- Fuzzy threshold has not been optimized experimentally.