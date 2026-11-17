# Nahuatl Retrieval Development Experiment v0.1

## Corpus

Real Nahuatl lexical corpus.

- Source records: 10,891
- Valid lexical entries: 10,891
- Rejected records: 0
- Canonical forms: 10,500
- Unique canonical forms: 10,144
- Ambiguous canonical forms: 356

## Evaluation dataset

Automatically generated development robustness set.

- Queries: 50
- Categories: 10
- Queries per category: 5

This dataset is not considered the final linguistic gold
standard.

## Retrieval methods

### B0 — Exact Raw

Direct matching against the original headword.

### B1 — Exact Normalized

Exact matching after conservative Unicode normalization.

### B2 — Fuzzy Normalized

Normalized Levenshtein similarity.

Parameters:

- threshold: 0.60
- top_k: 5

## Overall results

| Method | Top-1 | P@1 | P@5 | Recall@5 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|---:|---:|
| B0 | 0.3000 | 0.3000 | 0.0800 | 0.3000 | 0.3000 | 0.3000 |
| B1 | 0.4800 | 0.4800 | 0.1200 | 0.5000 | 0.4900 | 0.4926 |
| B2 | 0.8800 | 0.8800 | 0.2200 | 1.0000 | 0.9317 | 0.9491 |

## B2 error analysis

B2 produced six Top-1 errors.

### Exact

`kantabria`

The expected lowercase entry was ranked second because
normalization maps `kantabria` and `Kantabria` to the same
normalized representation.

### Insertion

`iluikatlaatilistli`

Expected:

`iluikatlatilistli`

A competing lexical item received a higher Levenshtein
similarity score.

### Substitution

`atlxko`

Expected:

`atlako`

`Atlixko` received a higher similarity score.

### Transposition

`chiaiutl`

Expected:

`chiauitl`

Relevant rank: 4.

### Transposition

`isutal`

Expected:

`isuatl`

Relevant rank: 3.

Standard Levenshtein distance does not model adjacent
transposition as a single edit operation.

### Diacritic

`tlatia (tlatia)`

Expected:

`tlatia (tlātiā)`

A competing form with a different diacritic pattern was
ranked first.

## Interpretation

B2 retrieved at least one relevant entry in the first five
positions for every development query.

The main remaining problem is therefore ranking rather than
candidate retrieval.

Observed error sources include:

- normalization collisions,
- lexical competitors,
- adjacent transpositions,
- diacritic variation.

No parameter optimization was performed after observing
these results.