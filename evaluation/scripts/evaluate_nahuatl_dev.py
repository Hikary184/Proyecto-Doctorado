import csv
import json
import math

from collections import defaultdict
from pathlib import Path

from src.retrieval.cascade import (
    search_cascade
)

from src.models.lexical_entry import (
    LexicalEntry
)

from src.retrieval.exact import (
    search_exact_raw,
    search_exact_normalized
)

from src.retrieval.fuzzy import (
    search_fuzzy_normalized
)

from src.retrieval.damerau import (
    search_damerau_normalized
)

from src.retrieval.cascade_damerau import (
    search_cascade_damerau
)


CORPUS_FILE = Path(
    "data/processed/nahuatl/"
    "nahuatl_entries.json"
)

QUERY_FILE = Path(
    "evaluation/gold/"
    "nahuatl_dev_queries_v0_1.json"
)

OUTPUT_DIR = Path(
    "results/tables"
)

TOP_K = 5

FUZZY_THRESHOLD = 0.60


# ============================================================
# METRICS
# ============================================================


def metric_top1(
    retrieved_ids,
    relevant_ids
):

    if not retrieved_ids:
        return 0.0

    return (
        1.0
        if retrieved_ids[0] in relevant_ids
        else 0.0
    )


def metric_precision_at_k(
    retrieved_ids,
    relevant_ids,
    k
):

    top_k = retrieved_ids[:k]

    hits = sum(
        1
        for entry_id in top_k
        if entry_id in relevant_ids
    )

    return hits / k


def metric_recall_at_k(
    retrieved_ids,
    relevant_ids,
    k
):

    if not relevant_ids:
        return 0.0

    top_k = retrieved_ids[:k]

    hits = sum(
        1
        for entry_id in top_k
        if entry_id in relevant_ids
    )

    return (
        hits
        /
        len(relevant_ids)
    )


def metric_reciprocal_rank(
    retrieved_ids,
    relevant_ids
):

    for rank, entry_id in enumerate(
        retrieved_ids,
        start=1
    ):

        if entry_id in relevant_ids:

            return 1.0 / rank

    return 0.0


def metric_ndcg_at_k(
    retrieved_ids,
    relevant_ids,
    k
):

    top_k = retrieved_ids[:k]

    dcg = 0.0

    for index, entry_id in enumerate(
        top_k,
        start=1
    ):

        if entry_id in relevant_ids:

            dcg += (
                1.0
                /
                math.log2(index + 1)
            )

    ideal_relevant = min(
        len(relevant_ids),
        k
    )

    if ideal_relevant == 0:
        return 0.0

    idcg = 0.0

    for index in range(
        1,
        ideal_relevant + 1
    ):

        idcg += (
            1.0
            /
            math.log2(index + 1)
        )

    return dcg / idcg


# ============================================================
# LOAD DATA
# ============================================================


def load_corpus():

    with open(
        CORPUS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return [
        LexicalEntry.model_validate(
            item
        )
        for item in data
    ]


def load_queries():

    with open(
        QUERY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# RETRIEVAL METHODS
# ============================================================


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
            top_k=TOP_K,
            threshold=FUZZY_THRESHOLD
        )

    if method_name == "B3_cascade":

        return search_cascade(
            query,
            entries,
            top_k=TOP_K,
            threshold=FUZZY_THRESHOLD
        )

    if method_name == "B4_damerau_normalized":

        return search_damerau_normalized(
            query,
            entries,
            top_k=TOP_K,
            threshold=FUZZY_THRESHOLD
        )
    if method_name == "B5_cascade_damerau":

        return search_cascade_damerau(
            query,
            entries,
            top_k=TOP_K,
            threshold=FUZZY_THRESHOLD
        )

    raise ValueError(
        f"Unknown method: {method_name}"
    )


# ============================================================
# SAVE CSV
# ============================================================


def save_csv(
    path,
    rows
):

    if not rows:
        return

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


# ============================================================
# MAIN
# ============================================================


def main():

    print()
    print("NAHUATL RETRIEVAL EVALUATION")
    print("=" * 72)

    entries = load_corpus()

    queries = load_queries()

    print(
        f"Corpus entries: {len(entries)}"
    )

    print(
        f"Evaluation queries: {len(queries)}"
    )

    print(
        f"Fuzzy threshold: {FUZZY_THRESHOLD}"
    )

    print(
        f"Top K: {TOP_K}"
    )

    methods = [
        "B0_exact_raw",
        "B1_exact_normalized",
        "B2_fuzzy_normalized",
        "B3_cascade",
        "B4_damerau_normalized",
        "B5_cascade_damerau"
    ]

    detailed_rows = []

    # --------------------------------------------------------
    # Execute evaluation
    # --------------------------------------------------------

    for query_data in queries:

        query_id = (
            query_data["query_id"]
        )

        query_text = (
            query_data["query"]
        )

        category = (
            query_data["category"]
        )

        source_headword = (
            query_data[
                "source_headword"
            ]
        )

        relevant_ids = set(
            query_data["relevant_ids"]
        )

        for method_name in methods:

            results = run_method(
                method_name,
                query_text,
                entries
            )

            retrieved_ids = [
                result.entry_id
                for result in results
            ]

            top1 = metric_top1(
                retrieved_ids,
                relevant_ids
            )

            precision_1 = (
                metric_precision_at_k(
                    retrieved_ids,
                    relevant_ids,
                    1
                )
            )

            precision_5 = (
                metric_precision_at_k(
                    retrieved_ids,
                    relevant_ids,
                    TOP_K
                )
            )

            recall_5 = (
                metric_recall_at_k(
                    retrieved_ids,
                    relevant_ids,
                    TOP_K
                )
            )

            rr = metric_reciprocal_rank(
                retrieved_ids,
                relevant_ids
            )

            ndcg_5 = metric_ndcg_at_k(
                retrieved_ids,
                relevant_ids,
                TOP_K
            )

            if results:

                top_result_id = (
                    results[0].entry_id
                )

                top_result_headword = (
                    results[0].headword
                )

                top_result_score = (
                    results[0].score
                )

            else:

                top_result_id = ""
                top_result_headword = ""
                top_result_score = 0.0

            detailed_rows.append({

                "query_id":
                    query_id,

                "category":
                    category,

                "query":
                    query_text,

                "source_headword":
                    source_headword,

                "method":
                    method_name,

                "relevant_count":
                    len(relevant_ids),

                "returned_count":
                    len(results),

                "top_result_id":
                    top_result_id,

                "top_result_headword":
                    top_result_headword,

                "top_result_score":
                    top_result_score,

                "top1_accuracy":
                    top1,

                "precision_at_1":
                    precision_1,

                "precision_at_5":
                    precision_5,

                "recall_at_5":
                    recall_5,

                "mrr":
                    rr,

                "ndcg_at_5":
                    ndcg_5,

                "relevant_ids":
                    "|".join(
                        sorted(relevant_ids)
                    ),

                "retrieved_ids":
                    "|".join(
                        retrieved_ids
                    )
            })

    # --------------------------------------------------------
    # General summary
    # --------------------------------------------------------

    summary_rows = []

    for method_name in methods:

        method_rows = [
            row
            for row in detailed_rows
            if row["method"]
            == method_name
        ]

        count = len(
            method_rows
        )

        summary_rows.append({

            "method":
                method_name,

            "queries":
                count,

            "top1_accuracy":
                sum(
                    row["top1_accuracy"]
                    for row in method_rows
                ) / count,

            "precision_at_1":
                sum(
                    row["precision_at_1"]
                    for row in method_rows
                ) / count,

            "precision_at_5":
                sum(
                    row["precision_at_5"]
                    for row in method_rows
                ) / count,

            "recall_at_5":
                sum(
                    row["recall_at_5"]
                    for row in method_rows
                ) / count,

            "mrr":
                sum(
                    row["mrr"]
                    for row in method_rows
                ) / count,

            "ndcg_at_5":
                sum(
                    row["ndcg_at_5"]
                    for row in method_rows
                ) / count
        })

    # --------------------------------------------------------
    # Category summary
    # --------------------------------------------------------

    grouped = defaultdict(list)

    for row in detailed_rows:

        key = (
            row["method"],
            row["category"]
        )

        grouped[key].append(
            row
        )

    category_rows = []

    for (
        method_name,
        category
    ), rows in sorted(
        grouped.items()
    ):

        count = len(rows)

        category_rows.append({

            "method":
                method_name,

            "category":
                category,

            "queries":
                count,

            "top1_accuracy":
                sum(
                    row["top1_accuracy"]
                    for row in rows
                ) / count,

            "precision_at_1":
                sum(
                    row["precision_at_1"]
                    for row in rows
                ) / count,

            "precision_at_5":
                sum(
                    row["precision_at_5"]
                    for row in rows
                ) / count,

            "recall_at_5":
                sum(
                    row["recall_at_5"]
                    for row in rows
                ) / count,

            "mrr":
                sum(
                    row["mrr"]
                    for row in rows
                ) / count,

            "ndcg_at_5":
                sum(
                    row["ndcg_at_5"]
                    for row in rows
                ) / count
        })

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    detailed_file = (
        OUTPUT_DIR
        /
        "nahuatl_dev_detailed.csv"
    )

    summary_file = (
        OUTPUT_DIR
        /
        "nahuatl_dev_summary.csv"
    )

    category_file = (
        OUTPUT_DIR
        /
        "nahuatl_dev_by_category.csv"
    )

    save_csv(
        detailed_file,
        detailed_rows
    )

    save_csv(
        summary_file,
        summary_rows
    )

    save_csv(
        category_file,
        category_rows
    )

    # --------------------------------------------------------
    # Console report
    # --------------------------------------------------------

    print()
    print("OVERALL RESULTS")
    print("=" * 72)

    for row in summary_rows:

        print()
        print(
            row["method"]
        )

        print(
            f"  Top-1      : "
            f"{row['top1_accuracy']:.4f}"
        )

        print(
            f"  P@1        : "
            f"{row['precision_at_1']:.4f}"
        )

        print(
            f"  P@5        : "
            f"{row['precision_at_5']:.4f}"
        )

        print(
            f"  Recall@5   : "
            f"{row['recall_at_5']:.4f}"
        )

        print(
            f"  MRR        : "
            f"{row['mrr']:.4f}"
        )

        print(
            f"  nDCG@5     : "
            f"{row['ndcg_at_5']:.4f}"
        )

    print()
    print("RESULTS BY CATEGORY")
    print("=" * 72)

    for row in category_rows:

        print(
            f"{row['method']:24} "
            f"{row['category']:15} "
            f"Top1={row['top1_accuracy']:.2f} "
            f"R@5={row['recall_at_5']:.2f} "
            f"MRR={row['mrr']:.2f} "
            f"nDCG={row['ndcg_at_5']:.2f}"
        )

    print()
    print("FILES")
    print("=" * 72)

    print(
        f"Detailed: {detailed_file}"
    )

    print(
        f"Summary:  {summary_file}"
    )

    print(
        f"Category: {category_file}"
    )

    print()
    print(
        "NOTE: Results correspond to the "
        "automatically generated development "
        "robustness set, not to the final "
        "linguistic gold standard."
    )


if __name__ == "__main__":
    main()