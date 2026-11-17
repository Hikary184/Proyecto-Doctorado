# Nahuatl Retrieval Development Experiment v0.3

## Objective

Compare normalized Levenshtein and Damerau-Levenshtein
retrieval on the same Nahuatl development dataset.

## Corpus

- 10,891 lexical entries
- 10,500 canonical forms
- 10,144 unique canonical forms
- 356 ambiguous canonical forms

## Evaluation set

- 50 automatically generated development queries
- 10 categories
- 5 queries per category

This is not the final linguistic gold standard.

## Methods

B0 — Exact raw retrieval

B1 — Exact normalized retrieval

B2 — Normalized Levenshtein

B3 — Cascaded retrieval:
1. exact raw
2. exact normalized
3. fuzzy Levenshtein

B4 — Normalized Damerau-Levenshtein

Fuzzy parameters:

- threshold: 0.60
- top_k: 5

## Results

| Method | Top-1 | Recall@5 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|
| B0 | 0.3000 | 0.3000 | 0.3000 | 0.3000 |
| B1 | 0.4800 | 0.5000 | 0.4900 | 0.4926 |
| B2 | 0.8800 | 1.0000 | 0.9317 | 0.9491 |
| B3 | 0.9000 | 1.0000 | 0.9417 | 0.9565 |
| B4 | 0.9200 | 1.0000 | 0.9600 | 0.9705 |

## Main finding

Damerau-Levenshtein improved the transposition category
from Top-1 = 0.60 with standard Levenshtein to Top-1 = 1.00.

The improvement supports treating adjacent character
transpositions differently from ordinary insertions,
deletions and substitutions.

B4 still produced Top-1 errors in other categories.

No parameter optimization was performed after observing
these results.