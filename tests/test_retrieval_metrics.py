from evaluation.metrics.retrieval_metrics import (
    top1_accuracy,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    ndcg_at_k
)


def test_top1_correct():

    retrieved = [
        "a",
        "b",
        "c"
    ]

    relevant = [
        "a"
    ]

    assert (
        top1_accuracy(
            retrieved,
            relevant
        )
        == 1.0
    )


def test_top1_incorrect():

    retrieved = [
        "b",
        "a"
    ]

    relevant = [
        "a"
    ]

    assert (
        top1_accuracy(
            retrieved,
            relevant
        )
        == 0.0
    )


def test_recall_at_5():

    retrieved = [
        "x",
        "a",
        "y"
    ]

    relevant = [
        "a"
    ]

    assert (
        recall_at_k(
            retrieved,
            relevant,
            5
        )
        == 1.0
    )


def test_reciprocal_rank():

    retrieved = [
        "x",
        "a",
        "y"
    ]

    relevant = [
        "a"
    ]

    assert (
        reciprocal_rank(
            retrieved,
            relevant
        )
        == 0.5
    )


def test_ndcg_perfect():

    retrieved = [
        "a",
        "x"
    ]

    relevant = [
        "a"
    ]

    assert (
        ndcg_at_k(
            retrieved,
            relevant,
            5
        )
        == 1.0
    )