import json

from evaluation_ground_truth import GROUND_TRUTH


def precision_at_k(
    predicted,
    relevant,
    k=10
):

    predicted = predicted[:k]

    if not predicted:
        return 0.0

    relevant_set = set(relevant)

    hits = sum(
        1
        for candidate in predicted
        if candidate in relevant_set
    )

    return hits / len(predicted)


def recall_at_k(
    predicted,
    relevant,
    k=10
):

    predicted = predicted[:k]

    if not relevant:
        return 0.0

    relevant_set = set(relevant)

    hits = sum(
        1
        for candidate in predicted
        if candidate in relevant_set
    )

    return hits / len(relevant_set)


def main():

    with open(
        "evaluation_results.json",
        "r",
        encoding="utf-8"
    ) as file:

        results = json.load(file)

    print("=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    total_precision = 0.0
    total_recall = 0.0

    count = 0

    for result in results:

        job_file = result["job_file"]

        predicted = [
            item["candidate_name"]
            for item in result["top_matches"]
        ]

        relevant = GROUND_TRUTH.get(
            job_file,
            []
        )

        precision = precision_at_k(
            predicted,
            relevant,
            10
        )

        recall = recall_at_k(
            predicted,
            relevant,
            10
        )

        total_precision += precision
        total_recall += recall

        count += 1

        print("\nJob:", job_file)

        print(
            f"Precision@10: "
            f"{precision:.2%}"
        )

        print(
            f"Recall@10: "
            f"{recall:.2%}"
        )

    print("\n" + "=" * 70)

    print(
        f"Average Precision@10: "
        f"{total_precision / count:.2%}"
    )

    print(
        f"Average Recall@10: "
        f"{total_recall / count:.2%}"
    )


if __name__ == "__main__":
    main()