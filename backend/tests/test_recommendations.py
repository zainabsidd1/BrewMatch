from types import SimpleNamespace

import httpx

from personalized_recs import (
    _combo_catalog_description,
    _logged_drink_keys,
    generate_exploration_recommendation,
    generate_familiar_recommendation,
    generate_personalized_recommendations,
)
from taste_profile import build_user_taste_profile


def _log(
    drink_id: str,
    drink_name: str,
    rating: int,
    notes: str = "",
    temperature: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        drink_id=drink_id,
        drink_name=drink_name,
        rating=rating,
        notes=notes,
        temperature=temperature,
    )


def test_highly_rated_iced_drinks_push_profile_toward_iced():
    logs = [
        _log("iced-americano", "Iced Americano", 5),
        _log("iced-americano", "Iced Americano", 5),
        _log("cold-brew", "Cold Brew", 5),
    ]

    profile = build_user_taste_profile(logs)

    assert profile.preferred_temperature == "iced"
    assert profile.temperature_mix["iced"] > profile.temperature_mix["hot"]


def test_logged_hot_and_iced_drinks_count_in_temperature_mix():
    logs = [
        _log("latte", "Caramel Latte", 5, temperature="hot"),
        _log("latte", "Vanilla Latte", 4, temperature="iced"),
    ]

    profile = build_user_taste_profile(logs)

    assert profile.temperature_mix["hot"] > 0
    assert profile.temperature_mix["iced"] > 0


def test_syrup_and_sweet_drinks_shape_sweetness_mix():
    logs = [
        _log("latte", "Latte", 5),
        _log("latte", "Vanilla Latte", 5),
        _log("biscoff-latte", "Biscoff Latte", 5),
        _log("mocha", "Iced Mocha", 4),
    ]

    profile = build_user_taste_profile(logs)

    assert profile.sweetness_mix["low"] > 0
    assert profile.sweetness_mix["medium"] > 0
    assert profile.sweetness_mix["high"] > 0
    assert profile.sweetness_mix["high"] > profile.sweetness_mix["low"]


def test_low_ratings_negatively_affect_related_preferences():
    logs = [
        _log("mocha", "Mocha", 1),
        _log("mocha", "Mocha", 1),
        _log("biscoff-latte", "Biscoff Latte", 1),
    ]

    profile = build_user_taste_profile(logs)

    assert "mocha" in profile.disliked_base_ids
    assert "chocolate" not in profile.preferred_flavors
    assert "biscoff" not in profile.preferred_flavors
    assert profile.flavor_scores.get("chocolate", 0) < 0


def test_what_you_might_like_follows_historical_taste_trends():
    logs = [
        _log("iced-americano", "Iced Americano", 5),
        _log("iced-americano", "Iced Americano", 5),
        _log("iced-americano", "Iced Americano", 4),
    ]
    profile = build_user_taste_profile(logs)

    recommendation = generate_familiar_recommendation(profile, logs)

    assert recommendation.temperature == "iced"
    assert recommendation.drink_id in {"americano", *profile.liked_base_ids}


def test_try_something_new_is_a_random_untried_drink(monkeypatch):
    from personalized_recs import DrinkCombination

    logs = [
        _log("latte", "Latte", 5),
        _log("latte", "Vanilla Latte", 4),
        _log("iced-americano", "Iced Americano", 5),
    ]
    profile = build_user_taste_profile(logs)
    familiar = DrinkCombination(
        drink_id="latte",
        base_drink="Latte",
        temperature="hot",
        sweetness="low",
        syrup=None,
        modifier=None,
    )
    captured: list = []

    def _choice(seq):
        captured.extend(seq)
        return seq[0]

    monkeypatch.setattr("personalized_recs.random.choice", _choice)

    recommendation = generate_exploration_recommendation(profile, logs, familiar)

    logged_keys = _logged_drink_keys(logs)
    candidate_keys = {combo.drink_key for combo in captured}

    assert recommendation.drink_key not in logged_keys
    assert recommendation.drink_key != familiar.drink_key
    assert ("latte", "hot", "") not in candidate_keys
    assert ("latte", "hot", "vanilla") not in candidate_keys
    assert ("americano", "iced", "") not in candidate_keys
    assert ("latte", "iced", "") in candidate_keys
    assert ("latte", "hot", "caramel") in candidate_keys
    assert ("americano", "hot", "") in candidate_keys


def test_try_something_new_uses_catalog_description(monkeypatch):
    from coffee_catalog import COFFEE_DRINKS
    from personalized_recs import DrinkCombination

    combo = DrinkCombination(
        drink_id="cold-brew",
        base_drink="Cold Brew",
        temperature="iced",
        sweetness="low",
        syrup=None,
        modifier=None,
    )
    monkeypatch.setattr(
        "personalized_recs.generate_exploration_recommendation",
        lambda *_args, **_kwargs: combo,
    )

    logs = [
        _log("iced-americano", "Iced Americano", 5),
        _log("latte", "Latte", 4),
    ]
    result = generate_personalized_recommendations(logs)
    catalog = next(drink for drink in COFFEE_DRINKS if drink["id"] == "cold-brew")

    assert result["try_something_new"]["explanation"] == catalog["description"]
    assert result["try_something_new"]["explanation"] == _combo_catalog_description(
        combo
    )


def test_zero_history_returns_fallback_state(monkeypatch):
    from personalized_recs import DrinkCombination, ALL_COMBINATIONS

    monkeypatch.setattr(
        "personalized_recs.random.choice",
        lambda seq: ALL_COMBINATIONS[0],
    )

    result = generate_personalized_recommendations([])

    assert result["what_you_might_like"] is None
    assert result["try_something_new"] is not None
    assert result["try_something_new"]["drink_id"]
    assert result["taste_profile"]["rated_count"] == 0
    assert isinstance(ALL_COMBINATIONS[0], DrinkCombination)


def test_ollama_timeout_does_not_break_recommendations(monkeypatch):
    logs = [
        _log("iced-americano", "Iced Americano", 5),
        _log("latte", "Iced Latte", 4),
    ]

    monkeypatch.setattr("personalized_recs._ollama_available", lambda: True)

    def _timeout(prompt: str) -> str:
        raise httpx.TimeoutException("Ollama timed out")

    monkeypatch.setattr("personalized_recs._call_ollama", _timeout)

    result = generate_personalized_recommendations(logs)

    assert result["what_you_might_like"] is not None
    assert result["try_something_new"] is not None
    assert result["what_you_might_like"]["explanation"]
    assert result["try_something_new"]["explanation"]
