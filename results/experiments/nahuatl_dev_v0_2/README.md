# Nahuatl Retrieval Development Experiment v0.2

## Objective

Evaluate whether a cascaded retrieval strategy improves
ranking compared with fuzzy normalized retrieval.

## Corpus

- 10,891 lexical entries
- 10,500 canonical forms
- 10,144 unique canonical forms
- 356 ambiguous forms

## Development dataset

- 50 automatically generated robustness queries
- 10 categories
- 5 queries per category

This is a development set and is not the final linguistic
gold standard.

## Methods

### B0
Exact raw retrieval.

### B1
Exact normalized retrieval.

### B2
Normalized Levenshtein retrieval.

Parameters:

- threshold: 0.60
- top_k: 5

### B3
Cascaded retrieval:

1. exact raw
2. exact normalized
3. fuzzy normalized

## Results

| Method | Top-1 | Recall@5 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|
| B0 | 0.3000 | 0.3000 | 0.3000 | 0.3000 |
| B1 | 0.4800 | 0.5000 | 0.4900 | 0.4926 |
| B2 | 0.8800 | 1.0000 | 0.9317 | 0.9491 |
| B3 | 0.9000 | 1.0000 | 0.9417 | 0.9565 |

## Interpretation

B3 improves Top-1 accuracy from 0.88 to 0.90.

The improvement corresponds to one exact-match query that
was incorrectly ranked by B2 because normalization caused a
case-based collision.

B3 preserves exact raw matches before applying normalization.

No improvement was observed for deletion, insertion,
substitution, transposition or diacritic categories.

The results therefore indicate that cascade retrieval solves
a specific ranking problem rather than improving approximate
matching in general.

No parameter optimization was performed.