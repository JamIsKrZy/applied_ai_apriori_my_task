import ast
from collections import defaultdict
from itertools import combinations


def get_product_set(records) -> set:
    return {
        product for entity in records for product in ast.literal_eval(entity["Product"])
    }


def filter_validate_support(k_1_list: list[dict], support) -> list[dict]:
    """
    from list of k-1 items, filter out the accepted records
    """
    accepted_k1_list = []
    for item in k_1_list:
        if item["support"] >= support:
            accepted_k1_list.append(item)

    return accepted_k1_list


def get_k_1(records) -> list[dict]:
    """
    Extracts the k-1 itemsets from the given records.
    returns {
        'product': 'Product Name',
        'frequency': 5,
        'support': 0.05
    }
    """
    product_set = get_product_set(records)
    total_records = len(records)

    k_1_list = []

    for product in product_set:
        frequency = sum(
            1 for entity in records if product in ast.literal_eval(entity["Product"])
        )
        support = frequency / total_records
        k_1_list.append(
            {"product": product, "frequency": frequency, "support": support}
        )

    return k_1_list


def get_k_2(
    accepted_k_1: list[dict],
    records: list[dict],
) -> list[dict]:
    """
    Generates 2-itemsets from accepted k=1 itemsets
    and calculates their frequency and support.
    """
    total_records = len(records)

    if total_records == 0 or len(accepted_k_1) < 2:
        return []

    # 1. Candidate generation: extract individual product names.
    frequent_items = [item["product"] for item in accepted_k_1]

    candidates = {frozenset(combo) for combo in combinations(frequent_items, 2)}

    # 2. Support counting.
    candidate_counts = defaultdict(int)

    for entity in records:
        basket = set(ast.literal_eval(entity.get("Product", "[]")))

        # Generate unique pairs from this basket.
        basket_pairs = {frozenset(combo) for combo in combinations(basket, 2)}

        # Count only candidate pairs.
        for pair in basket_pairs.intersection(candidates):
            candidate_counts[pair] += 1

    # 3. Format the result.
    k_2_list = []

    for pair, frequency in candidate_counts.items():
        k_2_list.append(
            {
                "product": pair,
                "frequency": frequency,
                "support": frequency / total_records,
            }
        )

    return k_2_list
