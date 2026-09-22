import csv
import json

from pathlib import Path
from statistics import mean

from src.retrieval.corpus import (
    load_corpus
)

from src.retrieval.exact import (
    search_exact_raw,
    search_exact_normalized
)

from src.retrieval.fuzzy import (
    search_fuzzy_normalized
)

from evaluation.metrics.retrieval_metrics import (
    top1_accuracy,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    ndcg_at_k
)


CORPUS_PATH = Path(
    "data/processed/"
    "sample_entries.normalized.json"
)

GOLD_PATH = Path(
    "evaluation/gold/"
    "baseline_queries.json"
)

RESULTS_DIR = Path(
    "results/tables"
)


def load_gold():

    with open(
        GOLD_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def extract_ids(results):

    return [
        result.entry_id
        for result in results
    ]


def run_method(
    method_name,
    query,
    entries
):

    if method_name == "B0_exact_raw":

        return search_exact_raw(
            query,
            entries
        )

    if method_name == "B1_exact_normalized":

        return search_exact_normalized(
            query,
            entries
        )

    if method_name == "B2_fuzzy_normalized":

        return search_fuzzy_normalized(
            query,
            entries,
            top_k=5,
            threshold=0.60
        )

    raise ValueError(
        f"Unknown method: {method_name}"
    )


def evaluate():

    entries = load_corpus(
        CORPUS_PATH
    )

    gold_queries = load_gold()

    methods = [
        "B0_exact_raw",
        "B1_exact_normalized",
        "B2_fuzzy_normalized"
    ]

    detailed_results = []

    for method in methods:

        for item in gold_queries:

            results = run_method(
                method,
                item["query"],
                entries
            )

            retrieved_ids = extract_ids(
                results
            )

            relevant_ids = item[
                "relevant_ids"
            ]

            row = {

                "method": method,

                "query_id": item["id"],

                "query": item["query"],

                "category": item["category"],

                "top1_accuracy":
                    top1_accuracy(
                        retrieved_ids,
                        relevant_ids
                    ),

                "precision_at_1":
                    precision_at_k(
                        retrieved_ids,
                        relevant_ids,
                        1
                    ),

                "precision_at_5":
                    precision_at_k(
                        retrieved_ids,
                        relevant_ids,
                        5
                    ),

                "recall_at_5":
                    recall_at_k(
                        retrieved_ids,
                        relevant_ids,
                        5
                    ),

                "mrr":
                    reciprocal_rank(
                        retrieved_ids,
                        relevant_ids
                    ),

                "ndcg_at_5":
                    ndcg_at_k(
                        retrieved_ids,
                        relevant_ids,
                        5
                    ),

                "retrieved_ids":
                    "|".join(
                        retrieved_ids
                    )
            }

            detailed_results.append(
                row
            )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    save_detailed_results(
        detailed_results
    )

    save_summary(
        detailed_results,
        methods
    )


def save_detailed_results(
    results
):

    output = (
        RESULTS_DIR /
        "baseline_detailed.csv"
    )

    fieldnames = list(
        results[0].keys()
    )

    with open(
        output,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print(
        f"Detailed results: {output}"
    )


def save_summary(
    results,
    methods
):

    summary_rows = []

    metric_names = [

        "top1_accuracy",
        "precision_at_1",
        "precision_at_5",
        "recall_at_5",
        "mrr",
        "ndcg_at_5"
    ]

    for method in methods:

        method_rows = [

            row
            for row in results
            if row["method"] == method
        ]

        summary = {
            "method": method
        }

        for metric in metric_names:

            summary[metric] = mean(
                row[metric]
                for row in method_rows
            )

        summary_rows.append(
            summary
        )

    output = (
        RESULTS_DIR /
        "baseline_summary.csv"
    )

    with open(
        output,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=summary_rows[
                0
            ].keys()
        )

        writer.writeheader()

        writer.writerows(
            summary_rows
        )

    print(
        f"Summary results: {output}"
    )

    print()

    print("BASELINE SUMMARY")

    print("=" * 72)

    for row in summary_rows:

        print()

        print(
            row["method"]
        )

        for metric in metric_names:

            print(
                f"  {metric:16s}: "
                f"{row[metric]:.4f}"
            )


if __name__ == "__main__":

    evaluate()