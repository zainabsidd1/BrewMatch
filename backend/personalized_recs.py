from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from typing import Any

from ai_match import _call_ollama, _ollama_available, _parse_ai_json, _soften_punctuation
from coffee_catalog import COFFEE_DRINKS
from drink_attributes import (
    DRINK_ATTRIBUTES,
    DrinkAttributes,
    Sweetness,
    Temperature,
    logged_syrup,
    logged_temperature,
    resolve_logged_drink,
)
from taste_profile import TasteProfile, build_user_taste_profile, profile_public_dict

logger = logging.getLogger(__name__)

SWEETNESS_LABEL = {"low": "low", "medium": "medium", "high": "high"}
EXPLORATION_SHORTLIST_SIZE = 5
JOURNAL_CONTEXT_LIMIT = 8


@dataclass(frozen=True)
class DrinkCombination:
    drink_id: str
    base_drink: str
    temperature: Temperature
    sweetness: Sweetness
    syrup: str | None
    modifier: str | None

    @property
    def key(self) -> tuple[str, str, str, str]:
        return (
            self.drink_id,
            self.temperature,
            self.syrup or "",
            self.modifier or "",
        )

    @property
    def drink_key(self) -> tuple[str, str, str]:
        return (self.drink_id, self.temperature, self.syrup or "")

    @property
    def display_name(self) -> str:
        syrup = f"{self.syrup.title()} " if self.syrup else ""
        name = self.base_drink
        if self.temperature == "iced" and not name.lower().startswith("iced"):
            return f"Iced {syrup}{name}".replace("  ", " ").strip()
        if syrup:
            return f"{syrup}{name}".strip()
        return name


def _effective_sweetness(attrs: DrinkAttributes, syrup: str | None) -> Sweetness:
    base = SWEETNESS_LABEL[attrs["default_sweetness"]]
    if not syrup:
        return base  # type: ignore[return-value]
    if base == "high":
        return "high"
    if base == "medium":
        return "high"
    return "medium"


def _iter_combinations() -> list[DrinkCombination]:
    combos: list[DrinkCombination] = []
    for attrs in DRINK_ATTRIBUTES.values():
        syrups: list[str | None] = [None, *attrs["compatible_syrups"]]
        modifiers: list[str | None] = [None, *attrs["compatible_modifiers"]]
        for temperature in attrs["temperatures"]:
            for syrup in syrups:
                if syrup and syrup == attrs["implied_syrup"]:
                    continue
                for modifier in modifiers:
                    combos.append(
                        DrinkCombination(
                            drink_id=attrs["id"],
                            base_drink=attrs["name"],
                            temperature=temperature,
                            sweetness=_effective_sweetness(attrs, syrup),
                            syrup=syrup,
                            modifier=modifier,
                        )
                    )
    return combos


ALL_COMBINATIONS = _iter_combinations()
PLAIN_COMBINATIONS = [combo for combo in ALL_COMBINATIONS if combo.modifier is None]


def _logged_combinations(logs: list[Any]) -> set[tuple[str, str, str, str]]:
    seen: set[tuple[str, str, str, str]] = set()
    for log in logs:
        base_id, attrs = resolve_logged_drink(log.drink_id, log.drink_name)
        temp = logged_temperature(
            log.drink_id,
            log.drink_name,
            attrs,
            getattr(log, "temperature", None),
        ) or attrs["default_temperature"]
        add_on = logged_syrup(log.drink_name, attrs)
        syrup = add_on or attrs["implied_syrup"]
        seen.add((base_id, temp, syrup or "", ""))
        seen.add((base_id, temp, "", ""))
    return seen


def _logged_drink_keys(logs: list[Any]) -> set[tuple[str, str, str]]:
    seen: set[tuple[str, str, str]] = set()
    for log in logs:
        base_id, attrs = resolve_logged_drink(log.drink_id, log.drink_name)
        temp = logged_temperature(
            log.drink_id,
            log.drink_name,
            attrs,
            getattr(log, "temperature", None),
        ) or attrs["default_temperature"]
        add_on = logged_syrup(log.drink_name, attrs)
        seen.add((base_id, temp, add_on or ""))
    return seen


def _score_combination(combo: DrinkCombination, profile: TasteProfile) -> float:
    attrs = DRINK_ATTRIBUTES[combo.drink_id]
    score = 0.0

    if profile.preferred_temperature:
        score += 3.0 if combo.temperature == profile.preferred_temperature else -2.0

    if profile.sweetness:
        gap = abs(
            {"low": 0, "medium": 1, "high": 2}[combo.sweetness]
            - {"low": 0, "medium": 1, "high": 2}[profile.sweetness]
        )
        score += 2.5 - gap * 1.8

    if profile.strength:
        gap = abs(
            {"mild": 0, "medium": 1, "bold": 2}[attrs["strength"]]
            - {"mild": 0, "medium": 1, "bold": 2}[profile.strength]
        )
        score += 2.0 - gap * 1.4

    milk_pref = profile.milk_preference
    milkiness = attrs["milkiness"]
    if milk_pref == "milk-forward":
        score += {"none": -2.5, "light": -0.5, "medium": 1.5, "high": 2.5}[milkiness]
    elif milk_pref == "espresso-forward":
        score += {"none": 2.5, "light": 1.8, "medium": 0.2, "high": -2.0}[milkiness]
    elif milk_pref == "balanced":
        score += {"none": -0.8, "light": 1.4, "medium": 2.2, "high": 0.8}[milkiness]

    if combo.syrup and combo.syrup in profile.preferred_flavors:
        score += 2.4
    if combo.syrup and combo.syrup in profile.avoided_flavors:
        score -= 3.0
    if attrs["implied_syrup"] and attrs["implied_syrup"] in profile.preferred_flavors:
        score += 1.8
    if attrs["implied_syrup"] and attrs["implied_syrup"] in profile.avoided_flavors:
        score -= 2.5

    if combo.drink_id in profile.liked_base_ids[:3]:
        score += 1.2
    if combo.drink_id in profile.disliked_base_ids:
        score -= 3.5

    if profile.strength in {"bold", "medium"} and combo.modifier == "extra shot":
        score += 0.8
    if profile.sweetness == "high" and combo.modifier in {"sweet cream", "whipped cream", "cold foam"}:
        score += 0.7
    if profile.milk_preference == "espresso-forward" and combo.modifier == "splash of milk":
        score += 0.6
    if profile.sweetness == "low" and combo.syrup:
        score -= 1.2
    if profile.sweetness == "low" and combo.modifier in {"sweet cream", "whipped cream"}:
        score -= 0.8

    return score


def generate_familiar_recommendation(
    profile: TasteProfile,
    logs: list[Any],
) -> DrinkCombination:
    logged = _logged_combinations(logs)
    most_logged_base = profile.liked_base_ids[0] if profile.liked_base_ids else None

    ranked = sorted(
        ALL_COMBINATIONS,
        key=lambda combo: (
            -_score_combination(combo, profile),
            combo.drink_id,
            combo.temperature,
            combo.syrup or "",
            combo.modifier or "",
        ),
    )

    for combo in ranked:
        # Avoid returning the exact logged default of their top drink with no twist.
        if (
            most_logged_base
            and combo.drink_id == most_logged_base
            and combo.syrup is None
            and combo.modifier is None
            and combo.key in logged
        ):
            continue
        return combo
    return ranked[0]


def _combo_sort_key(combo: DrinkCombination, profile: TasteProfile) -> tuple:
    return (
        -_score_combination(combo, profile),
        combo.drink_id,
        combo.temperature,
        combo.syrup or "",
        combo.modifier or "",
    )


def _untried_pool(
    combos: list[DrinkCombination],
    logged: set[tuple[str, str, str]],
    familiar_key: tuple[str, str, str] | None,
) -> list[DrinkCombination]:
    return [
        combo
        for combo in combos
        if combo.drink_key not in logged and combo.drink_key != familiar_key
    ]


def rank_exploration_candidates(
    profile: TasteProfile,
    logs: list[Any],
    familiar: DrinkCombination | None = None,
    limit: int = EXPLORATION_SHORTLIST_SIZE,
) -> list[tuple[DrinkCombination, float]]:
    """Heuristic retrieve: top untried combinations by taste-profile score."""
    logged = _logged_drink_keys(logs)
    familiar_key = familiar.drink_key if familiar is not None else None

    pools = [
        _untried_pool(PLAIN_COMBINATIONS, logged, familiar_key),
        _untried_pool(ALL_COMBINATIONS, logged, familiar_key),
        [
            combo
            for combo in PLAIN_COMBINATIONS
            if familiar is None or combo.drink_key != familiar_key
        ],
        list(ALL_COMBINATIONS),
    ]

    chosen: list[DrinkCombination] = []
    seen: set[tuple[str, str, str, str]] = set()
    for pool in pools:
        for combo in sorted(pool, key=lambda item: _combo_sort_key(item, profile)):
            if combo.key in seen:
                continue
            seen.add(combo.key)
            chosen.append(combo)
            if len(chosen) >= limit:
                return [
                    (item, _score_combination(item, profile)) for item in chosen
                ]

    return [(item, _score_combination(item, profile)) for item in chosen]


def generate_exploration_recommendation(
    profile: TasteProfile,
    logs: list[Any],
    familiar: DrinkCombination | None = None,
) -> DrinkCombination:
    ranked = rank_exploration_candidates(profile, logs, familiar)
    if ranked:
        return ranked[0][0]
    return generate_random_recommendation()


def _combo_public(combo: DrinkCombination, explanation: str) -> dict[str, Any]:
    return {
        "drink_id": combo.drink_id,
        "base_drink": combo.base_drink,
        "display_name": combo.display_name,
        "temperature": combo.temperature,
        "sweetness": combo.sweetness,
        "syrup": combo.syrup,
        "modifier": combo.modifier,
        "explanation": explanation,
    }


def _fallback_familiar_explanation(combo: DrinkCombination, profile: TasteProfile) -> str:
    temp = profile.preferred_temperature or combo.temperature
    sweet = profile.sweetness or combo.sweetness
    milk = profile.milk_preference or "balanced"
    flavors = ", ".join(profile.preferred_flavors[:2]) if profile.preferred_flavors else "clean coffee"
    extra = f" A {combo.modifier} keeps it in the strength range you usually enjoy." if combo.modifier else ""
    syrup = (
        f" {combo.syrup.title()} fits the flavors that show up in your higher ratings."
        if combo.syrup
        else ""
    )
    return (
        f"Your journal leans {temp} and {milk}, with {sweet} sweetness and a pull toward {flavors}. "
        f"{combo.display_name} stays close to that pattern without copying one past order.{syrup}{extra}"
    )


def _combo_catalog_description(combo: DrinkCombination) -> str:
    iced_id = f"iced-{combo.drink_id}"
    if combo.temperature == "iced":
        iced = next((drink for drink in COFFEE_DRINKS if drink["id"] == iced_id), None)
        if iced:
            return iced["description"]
    catalog = next((drink for drink in COFFEE_DRINKS if drink["id"] == combo.drink_id), None)
    if catalog:
        return catalog["description"]
    return combo.display_name


def generate_random_recommendation() -> DrinkCombination:
    pool = PLAIN_COMBINATIONS or ALL_COMBINATIONS
    return random.choice(pool)


def _explain_with_ollama(
    combo: DrinkCombination,
    profile: TasteProfile,
    kind: str,
) -> str | None:
    if not _ollama_available():
        return None

    novelty = (
        "Explain what makes this new compared with their usual logged drinks. "
        "Do not invent drinks or add-ons that are not in the recommendation."
        if kind == "explore"
        else "Explain why this combination fits their history. Do not invent extra add-ons."
    )
    prompt = (
        "You are BrewMatch. Write 2 to 3 warm, specific sentences.\n"
        "Never use em dashes. Never quote journal entries. Never sound like a chatbot.\n"
        f"{novelty}\n"
        "Return JSON only with key: explanation.\n\n"
        f"Recommendation: {combo.display_name}\n"
        f"Temperature: {combo.temperature}\n"
        f"Sweetness: {combo.sweetness}\n"
        f"Syrup: {combo.syrup or 'none'}\n"
        f"Modifier: {combo.modifier or 'none'}\n"
        f"Preferred temperature: {profile.preferred_temperature}\n"
        f"Sweetness preference: {profile.sweetness}\n"
        f"Strength: {profile.strength}\n"
        f"Milk preference: {profile.milk_preference}\n"
        f"Liked flavors: {', '.join(profile.preferred_flavors) or 'none'}\n"
        f"Liked bases: {', '.join(profile.liked_base_ids[:4]) or 'none'}\n"
    )
    try:
        content = _call_ollama(prompt)
        payload = _parse_ai_json(content)
        text = _soften_punctuation(str(payload.get("explanation", "")).strip())
        return text or None
    except Exception as exc:
        logger.warning("Ollama rec explanation failed (%s)", exc)
        return None


def _recent_journal_context(logs: list[Any], limit: int = JOURNAL_CONTEXT_LIMIT) -> str:
    def _sort_key(log: Any) -> tuple:
        tried = getattr(log, "date_tried", None)
        added = getattr(log, "date_added", None)
        return (tried or added or 0,)

    recent = sorted(logs, key=_sort_key, reverse=True)[:limit]
    lines: list[str] = []
    for log in recent:
        name = getattr(log, "drink_name", "unknown drink")
        rating = getattr(log, "rating", None)
        notes = str(getattr(log, "notes", None) or "").strip()
        rating_bit = f"rated {rating}/5" if rating is not None else "unrated"
        if notes:
            lines.append(f"- {name} ({rating_bit}): {notes[:220]}")
        else:
            lines.append(f"- {name} ({rating_bit})")
    return "\n".join(lines) if lines else "No journal entries."


def _rerank_exploration_with_ollama(
    shortlist: list[tuple[DrinkCombination, float]],
    profile: TasteProfile,
    logs: list[Any],
) -> tuple[DrinkCombination, str] | None:
    if len(shortlist) < 2 or not _ollama_available():
        return None

    numbered: list[str] = []
    for index, (combo, score) in enumerate(shortlist, start=1):
        numbered.append(
            f"{index}. {combo.display_name} | id={combo.drink_id} | "
            f"temp={combo.temperature} | sweetness={combo.sweetness} | "
            f"syrup={combo.syrup or 'none'} | modifier={combo.modifier or 'none'} | "
            f"heuristic_score={score:.2f}"
        )

    prompt = (
        "You are BrewMatch. Choose exactly one drink combination from the numbered "
        "shortlist. Do not invent drinks, syrups, or modifiers.\n"
        "These candidates are already untried. Pick the one that best fits the user's "
        "taste while still feeling like something new.\n"
        f"Return JSON only with keys: choice, explanation. choice must be an integer "
        f"from 1 to {len(shortlist)}.\n"
        "explanation: 2 to 3 warm sentences on why this pick beats the other shortlisted "
        "options. Never use em dashes. Never quote journal notes verbatim.\n\n"
        f"Preferred temperature: {profile.preferred_temperature}\n"
        f"Sweetness: {profile.sweetness}\n"
        f"Strength: {profile.strength}\n"
        f"Milk preference: {profile.milk_preference}\n"
        f"Liked flavors: {', '.join(profile.preferred_flavors) or 'none'}\n"
        f"Avoided flavors: {', '.join(profile.avoided_flavors) or 'none'}\n"
        f"Liked bases: {', '.join(profile.liked_base_ids[:4]) or 'none'}\n\n"
        f"Recent journal:\n{_recent_journal_context(logs)}\n\n"
        "Shortlist:\n"
        + "\n".join(numbered)
    )

    try:
        content = _call_ollama(prompt, temperature=0.15, num_predict=160)
        payload = _parse_ai_json(content)
        raw_choice = payload.get("choice")
        choice = int(raw_choice)
        if choice < 1 or choice > len(shortlist):
            raise ValueError(f"choice {choice} outside shortlist")
        text = _soften_punctuation(str(payload.get("explanation", "")).strip())
        if not text:
            raise ValueError("Missing explanation")
        return shortlist[choice - 1][0], text
    except Exception as exc:
        logger.warning("Ollama exploration rerank failed (%s)", exc)
        return None


def generate_personalized_recommendations(logs: list[Any]) -> dict[str, Any]:
    profile = build_user_taste_profile(logs)

    if len(logs) == 0:
        explore = generate_random_recommendation()
        return {
            "taste_profile": profile_public_dict(profile),
            "what_you_might_like": None,
            "try_something_new": _combo_public(
                explore,
                _combo_catalog_description(explore),
            ),
            "message": None,
        }

    familiar = generate_familiar_recommendation(profile, logs)
    shortlist = rank_exploration_candidates(profile, logs, familiar)
    explore = shortlist[0][0] if shortlist else generate_random_recommendation()

    familiar_text = _explain_with_ollama(familiar, profile, "familiar")
    if not familiar_text:
        familiar_text = _fallback_familiar_explanation(familiar, profile)

    reranked = _rerank_exploration_with_ollama(shortlist, profile, logs)
    if reranked is not None:
        explore, explore_text = reranked
    else:
        explore_text = _combo_catalog_description(explore)

    return {
        "taste_profile": profile_public_dict(profile),
        "what_you_might_like": _combo_public(familiar, familiar_text),
        "try_something_new": _combo_public(
            explore,
            explore_text,
        ),
        "message": None,
    }
