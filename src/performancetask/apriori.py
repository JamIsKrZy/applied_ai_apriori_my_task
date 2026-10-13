import ast
from collections import defaultdict
from itertools import combinations


def _as_product_set(product_value) -> set:
    if product_value is None:
        return set()

    if isinstance(product_value, str):
        parsed = ast.literal_eval(product_value)
        if isinstance(parsed, str):
            return {parsed}
        product_value = parsed

    if isinstance(product_value, (list, tuple, set)):
        return set(product_value)

    return {product_value}


def get_product_set(records) -> set:
    return {
        product
        for entity in records
        for product in _as_product_set(entity.get("Product", "[]"))
    }


def filter_validate_support(itemsets: list[dict], support) -> list[dict]:
    """
    Filter out itemsets whose support meets the minimum threshold.
    """
    accepted_itemsets = []
    for item in itemsets:
        if item.get("support", 0) >= support:
            accepted_itemsets.append(item)

    return accepted_itemsets


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

    for product in sorted(product_set):
        frequency = sum(
            1 for entity in records if product in _as_product_set(entity.get("Product", "[]"))
        )
        support = frequency / total_records if total_records else 0.0
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

    frequent_items = sorted({item["product"] for item in accepted_k_1})
    candidates = {frozenset(combo) for combo in combinations(frequent_items, 2)}

    if not candidates:
        return []

    candidate_counts = defaultdict(int)

    for entity in records:
        basket = _as_product_set(entity.get("Product", "[]"))
        basket_pairs = {frozenset(combo) for combo in combinations(sorted(basket), 2)}
        for pair in basket_pairs.intersection(candidates):
            candidate_counts[pair] += 1

    k_2_list = []
    for pair, frequency in sorted(candidate_counts.items(), key=lambda x: sorted(x[0])):
        k_2_list.append(
            {
                "product": pair,
                "frequency": frequency,
                "support": frequency / total_records,
            }
        )

    return k_2_list


def get_k_3(
    accepted_k_2: list[dict],
    records: list[dict],
) -> list[dict]:
    """
    Generates 3-itemsets from accepted k=2 itemsets,
    ensuring every 2-item subset is already frequent.
    """
    total_records = len(records)

    if total_records == 0 or len(accepted_k_2) < 3:
        return []

    candidate_pairs = {frozenset(item["product"]) for item in accepted_k_2}
    if not candidate_pairs:
        return []

    candidate_triplets = set()
    sorted_pairs = sorted(candidate_pairs, key=lambda item: tuple(sorted(item)))

    for left, right in combinations(sorted_pairs, 2):
        merged = set(left) | set(right)
        if len(merged) != 3:
            continue

        triplet = frozenset(merged)
        pair_combos = {
            frozenset(combo) for combo in combinations(sorted(triplet), 2)
        }

        if pair_combos.issubset(candidate_pairs):
            candidate_triplets.add(triplet)

    if not candidate_triplets:
        return []

    candidate_counts = defaultdict(int)
    for entity in records:
        basket = _as_product_set(entity.get("Product", "[]"))
        for triplet in candidate_triplets:
            if triplet.issubset(basket):
                candidate_counts[triplet] += 1

    k_3_list = []
    for triplet, frequency in sorted(candidate_counts.items(), key=lambda x: sorted(x[0])):
        k_3_list.append(
            {
                "product": triplet,
                "frequency": frequency,
                "support": frequency / total_records,
            }
        )

    return k_3_list


def generate_association_rules(
    frequent_itemsets: list[dict],
    min_confidence: float,
    min_support: float | None = None,
) -> list[dict]:
    """
    Builds association rules from frequent itemsets.
    Each rule is returned as a dictionary with:
    antecedent, consequent, support, confidence, lift.
    """
    if not frequent_itemsets:
        return []

    support_map = {}
    for item in frequent_itemsets:
        product = item["product"]
        if isinstance(product, str):
            item_key = frozenset({product})
        else:
            item_key = frozenset(product)
        support_map[item_key] = item["support"]

    generated_rules = set()
    rules = []

    for item in frequent_itemsets:
        product = item["product"]
        if isinstance(product, str):
            item_set = frozenset({product})
        else:
            item_set = frozenset(product)

        if len(item_set) < 2:
            continue

        for r in range(1, len(item_set)):
            for antecedent in combinations(sorted(item_set), r):
                antecedent_set = frozenset(antecedent)
                consequent_set = item_set - antecedent_set

                if not consequent_set:
                    continue

                antecedent_support = support_map.get(antecedent_set, 0.0)
                item_support = support_map.get(item_set, 0.0)
                consequent_support = support_map.get(consequent_set, 0.0)

                if antecedent_support <= 0 or item_support <= 0:
                    continue

                if min_support is not None and item_support < min_support:
                    continue

                confidence = item_support / antecedent_support
                if confidence < min_confidence:
                    continue

                lift = confidence / consequent_support if consequent_support else 0.0
                rule_key = (
                    tuple(sorted(antecedent_set)),
                    tuple(sorted(consequent_set)),
                )

                if rule_key in generated_rules:
                    continue

                generated_rules.add(rule_key)
                rules.append(
                    {
                        "antecedent": antecedent_set,
                        "consequent": consequent_set,
                        "support": item_support,
                        "confidence": confidence,
                        "lift": lift,
                    }
                )

    return sorted(
        rules,
        key=lambda rule: (-rule["confidence"], -rule["lift"], sorted(rule["antecedent"]), sorted(rule["consequent"])),
    )


get_association_rules = generate_association_rules
association_rules = generate_association_rules
