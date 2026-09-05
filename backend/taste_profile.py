from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from drink_attributes import (
    Sweetness,
    Temperature,
    logged_temperature,
    resolve_logged_drink,
)

RATING_WEIGHT = {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}

SWEETNESS_RANK = {"low": 0, "medium": 1, "high": 2}
STRENGTH_RANK = {"mild": 0, "medium": 1, "bold": 2}
MILK_RANK = {"none": 0, "light": 1, "medium": 2, "high": 3}

NOTE_FLAVORS = (
    "vanilla",
    "caramel",
    "hazelnut",
    "chocolate",
    "biscoff",
)


@dataclass
class TasteProfile:
    rated_count: int
    preferred_temperature: Temperature | None
    sweetness: Sweetness | None
    strength: str | None
    milk_preference: str | None
    preferred_flavors: list[str]
    avoided_flavors: list[str]
    liked_base_ids: list[str]
    disliked_base_ids: list[str]
    temperature_scores: dict[str, float] = field(default_factory=dict)
    sweetness_score: float = 0.0
    strength_score: float = 0.0
    milk_score: float = 0.0
    flavor_scores: dict[str, float] = field(default_factory=dict)
    base_scores: dict[str, float] = field(default_factory=dict)
    temperature_mix: dict[str, int] = field(default_factory=lambda: {"iced": 0, "hot": 0})
    sweetness_mix: dict[str, int] = field(default_factory=lambda: {"low": 0, "medium": 0, "high": 0})

    @property
    def confidence(self) -> str:
        if self.rated_count <= 0:
            return "none"
        if self.rated_count <= 2:
            return "low"
        return "full"


def _weight(rating: int | None) -> int:
    if rating is None:
        return 0
    return RATING_WEIGHT.get(int(rating), 0)


def _rank_to_label(value: float, mapping: dict[str, int]) -> str:
    closest = min(mapping.items(), key=lambda item: abs(item[1] - value))
    return closest[0]


def _to_percentages(counts: dict[str, float], keys: list[str]) -> dict[str, int]:
    values = [max(0.0, float(counts.get(key, 0.0))) for key in keys]
    total = sum(values)
    if total <= 0:
        return {key: 0 for key in keys}

    raw = [value / total * 100 for value in values]
    floors = [int(value) for value in raw]
    leftover = 100 - sum(floors)
    order = sorted(
        range(len(keys)),
        key=lambda index: raw[index] - floors[index],
        reverse=True,
    )
    for index in order[:leftover]:
        floors[index] += 1
    return {keys[index]: floors[index] for index in range(len(keys))}


def _mix_weight(log: Any) -> float:
    rating = getattr(log, "rating", None)
    if rating is None:
        return 1.0
    return float(max(1, int(rating)))


def _build_mixes(logs: list[Any]) -> tuple[dict[str, int], dict[str, int]]:
    temp_counts: dict[str, float] = {"iced": 0.0, "hot": 0.0}
    sweet_counts: dict[str, float] = {"low": 0.0, "medium": 0.0, "high": 0.0}

    for log in logs:
        weight = _mix_weight(log)
        _base_id, attrs = resolve_logged_drink(log.drink_id, log.drink_name)
        temp = logged_temperature(log.drink_id, log.drink_name, attrs)
        if temp:
            temp_counts[temp] = temp_counts.get(temp, 0.0) + weight
        sweetness = attrs["default_sweetness"]
        sweet_counts[sweetness] = sweet_counts.get(sweetness, 0.0) + weight

    return (
        _to_percentages(temp_counts, ["iced", "hot"]),
        _to_percentages(sweet_counts, ["low", "medium", "high"]),
    )


def _milk_label(rank: float) -> str:
    if rank < 1.0:
        return "espresso-forward"
    if rank < 2.2:
        return "balanced"
    return "milk-forward"


def build_user_taste_profile(logs: list[Any]) -> TasteProfile:
    temperature_mix, sweetness_mix = _build_mixes(logs)
    rated = [log for log in logs if getattr(log, "rating", None) is not None]
    temp_scores: dict[str, float] = defaultdict(float)
    flavor_scores: dict[str, float] = defaultdict(float)
    base_scores: dict[str, float] = defaultdict(float)
    sweetness_weighted = 0.0
    strength_weighted = 0.0
    milk_weighted = 0.0
    abs_weight = 0.0

    for log in rated:
        weight = _weight(log.rating)
        if weight == 0:
            abs_weight += 0.15
            continue

        magnitude = abs(weight)
        base_id, attrs = resolve_logged_drink(log.drink_id, log.drink_name)
        temp = logged_temperature(log.drink_id, log.drink_name, attrs)
        if temp:
            temp_scores[temp] += weight
        base_scores[base_id] += weight
        sweetness_weighted += SWEETNESS_RANK[attrs["default_sweetness"]] * weight
        strength_weighted += STRENGTH_RANK[attrs["strength"]] * weight
        milk_weighted += MILK_RANK[attrs["milkiness"]] * weight
        abs_weight += magnitude

        if attrs["implied_syrup"]:
            flavor_scores[attrs["implied_syrup"]] += weight

        notes = (getattr(log, "notes", None) or "").lower()
        for flavor in NOTE_FLAVORS:
            if flavor in notes:
                flavor_scores[flavor] += weight

    if abs_weight == 0:
        return TasteProfile(
            rated_count=len(rated),
            preferred_temperature=None,
            sweetness=None,
            strength=None,
            milk_preference=None,
            preferred_flavors=[],
            avoided_flavors=[],
            liked_base_ids=[],
            disliked_base_ids=[],
            temperature_mix=temperature_mix,
            sweetness_mix=sweetness_mix,
        )

    preferred_temp: Temperature | None = None
    if temp_scores:
        preferred_temp = max(temp_scores, key=temp_scores.get)  # type: ignore[arg-type]
        if temp_scores[preferred_temp] <= 0:
            preferred_temp = None

    sweetness_avg = sweetness_weighted / abs_weight
    strength_avg = strength_weighted / abs_weight
    milk_avg = milk_weighted / abs_weight

    preferred_flavors = [
        name
        for name, score in sorted(flavor_scores.items(), key=lambda item: item[1], reverse=True)
        if score > 0
    ]
    avoided_flavors = [
        name for name, score in flavor_scores.items() if score < 0
    ]
    liked_bases = [
        drink_id
        for drink_id, score in sorted(base_scores.items(), key=lambda item: item[1], reverse=True)
        if score > 0
    ]
    disliked_bases = [drink_id for drink_id, score in base_scores.items() if score < 0]

    return TasteProfile(
        rated_count=len(rated),
        preferred_temperature=preferred_temp,
        sweetness=_rank_to_label(sweetness_avg, SWEETNESS_RANK),  # type: ignore[arg-type]
        strength=_rank_to_label(strength_avg, STRENGTH_RANK),
        milk_preference=_milk_label(milk_avg),
        preferred_flavors=preferred_flavors[:3],
        avoided_flavors=avoided_flavors,
        liked_base_ids=liked_bases,
        disliked_base_ids=disliked_bases,
        temperature_scores=dict(temp_scores),
        sweetness_score=sweetness_avg,
        strength_score=strength_avg,
        milk_score=milk_avg,
        flavor_scores=dict(flavor_scores),
        base_scores=dict(base_scores),
        temperature_mix=temperature_mix,
        sweetness_mix=sweetness_mix,
    )


def profile_public_dict(profile: TasteProfile) -> dict[str, Any]:
    return {
        "preferred_temperature": profile.preferred_temperature,
        "sweetness": profile.sweetness,
        "preferred_flavors": profile.preferred_flavors,
        "strength": profile.strength,
        "milk_preference": profile.milk_preference,
        "confidence": profile.confidence,
        "rated_count": profile.rated_count,
        "temperature_mix": profile.temperature_mix,
        "sweetness_mix": profile.sweetness_mix,
    }
