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
        """Base + temperature + syrup. Modifier add-ons do not change the drink."""
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
        if attrs["implied_syrup"] and attrs["implied_syrup"] not in (attrs["compatible_syrups"]):
            # Implied flavor is part of the drink, not an add-on syrup.
            pass
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


def generate_exploration_recommendation(
    _profile: TasteProfile,
    logs: list[Any],
    familiar: DrinkCombination | None = None,
) -> DrinkCombination:
    logged = _logged_drink_keys(logs)
    familiar_key = familiar.drink_key if familiar is not None else None

    def _pool(combos: list[DrinkCombination]) -> list[DrinkCombination]:
        return [
            combo
            for combo in combos
            if combo.drink_key not in logged and combo.drink_key != familiar_key
        ]

    candidates = _pool(PLAIN_COMBINATIONS)
    if not candidates:
        candidates = _pool(ALL_COMBINATIONS)
    if not candidates:
        candidates = [
            combo
            for combo in PLAIN_COMBINATIONS
            if familiar is None or combo.drink_key != familiar_key
        ]
    if not candidates:
        candidates = ALL_COMBINATIONS
    return random.choice(candidates)


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
    explore = generate_exploration_recommendation(profile, logs, familiar)

    familiar_text = _explain_with_ollama(familiar, profile, "familiar")
    if not familiar_text:
        familiar_text = _fallback_familiar_explanation(familiar, profile)

    return {
        "taste_profile": profile_public_dict(profile),
        "what_you_might_like": _combo_public(familiar, familiar_text),
        "try_something_new": _combo_public(
            explore,
            _combo_catalog_description(explore),
        ),
        "message": None,
    }
