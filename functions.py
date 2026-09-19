import random
from collections import Counter
from typing import List, Dict, Any

# Constantes pour les scores (adaptées à tes règles)
SCORING_RULES = {
    "royal_suite": {"dice": {1, 2, 3, 4, 5, 6}, "score": 2000, "name": "Royal Suite"},
    "triple_1": {"min_count": 3, "score": 1000, "name": "Triple de 1"},
    "single_1": {"min_count": 1, "score_per_die": 100, "name": "1"},
    "single_5": {"min_count": 1, "score_per_die": 50, "name": "5"},
    "three_doubles": {"min_count": 3, "score": 500, "name": "3 Doubles"},
    "triple_other": {"min_count": 3, "score_per_die": 100, "name": "Triple de {die}"},
}

def throw(number_of_dices: int) -> List[int]:
    """Simule un lancer de dés."""
    return [random.randint(1, 6) for _ in range(number_of_dices)]

def get_scoring_options(throw_set: List[int]) -> List[Dict[str, Any]]:
    """
    Retourne toutes les options de scoring pour un lancer de dés.
    Si aucune combinaison valide n'est trouvée, retourne une liste vide.
    """
    options = []
    counts = Counter(throw_set)

    # 1. Royal Suite (1-2-3-4-5-6)
    if len(throw_set) == 6 and set(throw_set) == {1, 2, 3, 4, 5, 6}:
        options.append({
            "name": SCORING_RULES["royal_suite"]["name"],
            "score": SCORING_RULES["royal_suite"]["score"],
            "dice": throw_set.copy(),
            "remaining_dice": [],
        })

    # 2. Triples de 1
    count_of_1 = counts.get(1, 0)
    triples_of_1 = count_of_1 // 3
    remaining_1s = count_of_1 % 3

    if triples_of_1 > 0:
        options.append({
            "name": SCORING_RULES["triple_1"]["name"],
            "score": SCORING_RULES["triple_1"]["score"] * triples_of_1,
            "dice": [1] * (triples_of_1 * 3),
            "remaining_dice": [d for d in throw_set if d != 1 or (d == 1 and remaining_1s > 0 and [1] * remaining_1s not in [dice for opt in options for dice in [opt["dice"]]])],
        })
    if remaining_1s > 0:
        options.append({
            "name": f"{remaining_1s}x{SCORING_RULES['single_1']['name']}",
            "score": SCORING_RULES["single_1"]["score_per_die"] * remaining_1s,
            "dice": [1] * remaining_1s,
            "remaining_dice": [d for d in throw_set if d != 1],
        })

    # 3. Trois doubles (ex: 2 paires distinctes)
    doubles = [num for num, count in counts.items() if count >= 2]
    if len(doubles) >= 3:
        selected_doubles = doubles[:3]
        scoring_dice = []
        for die in selected_doubles:
            scoring_dice.extend([die] * 2)
        options.append({
            "name": SCORING_RULES["three_doubles"]["name"],
            "score": SCORING_RULES["three_doubles"]["score"],
            "dice": scoring_dice,
            "remaining_dice": [d for d in throw_set if d not in selected_doubles or throw_set.count(d) > 2],
        })

    # 4. Triples (autres que 1)
    for die in [2, 3, 4, 5, 6]:
        if counts.get(die, 0) >= 3:
            options.append({
                "name": SCORING_RULES["triple_other"]["name"].format(die=die),
                "score": SCORING_RULES["triple_other"]["score_per_die"] * die,
                "dice": [die] * 3,
                "remaining_dice": [d for d in throw_set if d != die] + [die] * (counts[die] - 3),
            })

    # 5. Dés simples (1 et 5)
    for die in [1, 5]:
        if die in counts:
            count = counts[die]
            if die == 1 and count < 3:
                options.append({
                    "name": f"{count}x{SCORING_RULES['single_1']['name']}",
                    "score": SCORING_RULES["single_1"]["score_per_die"] * count,
                    "dice": [die] * count,
                    "remaining_dice": [d for d in throw_set if d != die],
                })
            elif die == 5:
                options.append({
                    "name": f"{count}x{SCORING_RULES['single_5']['name']}",
                    "score": SCORING_RULES["single_5"]["score_per_die"] * count,
                    "dice": [die] * count,
                    "remaining_dice": [d for d in throw_set if d != die],
                })

    # Supprimer les doublons
    unique_options = []
    seen = set()
    for option in options:
        key = tuple(sorted(option["dice"]))
        if key not in seen:
            seen.add(key)
            unique_options.append(option)

    return unique_options