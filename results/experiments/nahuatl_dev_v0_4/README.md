# Nahuatl Orthographic Retrieval Development Experiment v0.4

## Purpose

Evaluate progressively more robust lexical retrieval
strategies on a real Nahuatl dictionary corpus.

## Corpus

- Lexical entries: 10,891
- Canonical forms: 10,500
- Unique canonical forms: 10,144
- Ambiguous canonical forms: 356
- Rejected source records: 0

## Development evaluation set

- 50 automatically generated robustness queries
- 10 categories
- 5 queries per category

This dataset is a development robustness set and is not
the final linguistic gold standard.

## Methods

### B0
Exact raw retrieval.

### B1
Exact retrieval after conservative normalization.

### B2
Normalized Levenshtein similarity.

### B3
Cascade:
1. exact raw
2. exact normalized
3. Levenshtein

### B4
Normalized Damerau-Levenshtein similarity.

### B5
Cascade:
1. exact raw
2. exact normalized
3. Damerau-Levenshtein

Fuzzy parameters:

- threshold: 0.60
- top_k: 5

## Overall results

| Method | Top-1 | Recall@5 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|
| B0 | 0.3000 | 0.3000 | 0.3000 | 0.3000 |
| B1 | 0.4800 | 0.5000 | 0.4900 | 0.4926 |
| B2 | 0.8800 | 1.0000 | 0.9317 | 0.9491 |
| B3 | 0.9000 | 1.0000 | 0.9417 | 0.9565 |
| B4 | 0.9200 | 1.0000 | 0.9600 | 0.9705 |
| B5 | 0.9400 | 1.0000 | 0.9700 | 0.9779 |

## Main findings

Conservative normalization substantially improves exact
retrieval for case and whitespace variation.

Approximate lexical matching substantially improves
robustness to character-level perturbations.

Cascaded retrieval protects exact source forms from ranking
collisions caused by normalization.

Damerau-Levenshtein improves adjacent character
transpositions relative to standard Levenshtein.

The combination of cascaded retrieval and
Damerau-Levenshtein obtained the highest Top-1 accuracy on
the development robustness set.

## Important limitation

The query set was generated automatically from existing
dictionary entries.

Therefore, these results measure controlled orthographic
robustness and must not be interpreted as evidence of
real-world search behavior by Nahuatl speakers.

No parameter optimization was performed after observing the
reported results.