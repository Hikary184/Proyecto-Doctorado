import math


def top1_accuracy(
    retrieved_ids: list[str],
    relevant_ids: list[str]
) -> float:

    if not retrieved_ids:
        return 0.0

    return float(
        retrieved_ids[0] in relevant_ids
    )


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int
) -> float:

    if k <= 0:
        raise ValueError(
            "k must be greater than zero."
        )

    retrieved_k = retrieved_ids[:k]

    hits = sum(
        1
        for entry_id in retrieved_k
        if entry_id in relevant_ids
    )

    return hits / k


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int
) -> float:

    if not relevant_ids:
        return 0.0

    retrieved_k = retrieved_ids[:k]

    hits = sum(
        1
        for entry_id in relevant_ids
        if entry_id in retrieved_k
    )

    return hits / len(relevant_ids)


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: list[str]
) -> float:

    for rank, entry_id in enumerate(
        retrieved_ids,
        start=1
    ):

        if entry_id in relevant_ids:
            return 1.0 / rank

    return 0.0


def ndcg_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int
) -> float:

    retrieved_k = retrieved_ids[:k]

    dcg = 0.0

    for index, entry_id in enumerate(
        retrieved_k
    ):

        relevance = (
            1.0
            if entry_id in relevant_ids
            else 0.0
        )

        dcg += relevance / math.log2(
            index + 2
        )

    ideal_hits = min(
        len(relevant_ids),
        k
    )

    if ideal_hits == 0:
        return 0.0

    idcg = sum(
        1.0 / math.log2(index + 2)
        for index in range(ideal_hits)
    )

    return dcg / idcg