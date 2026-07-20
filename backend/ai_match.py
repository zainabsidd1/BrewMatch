import json
import logging
import random
import re
from typing import Any

import httpx

from coffee_catalog import COFFEE_DRINKS, CoffeeDrink
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


def _catalog_for_prompt() -> str:
    """Compact catalog — local models struggle with long prompts."""
    lines: list[str] = []
    for drink in COFFEE_DRINKS:
        categories = ", ".join(drink["categories"])
        lines.append(f"- {drink['id']}: {drink['name']} [{categories}]")
    return "\n".join(lines)


def _answers_for_prompt(answers: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for index, item in enumerate(answers, start=1):
        lines.append(f"{index}. {item['option_label']}")
    return "\n".join(lines)


def _heuristic_match(answers: list[dict[str, Any]]) -> CoffeeDrink:
    """Scores drinks by answer keywords, with stronger weight on coffee-preference Qs."""
    text = " ".join(
        f"{item['question']} {item['option_label']}".lower() for item in answers
    )

    scores = {
        "Sweet": 0,
        "Bold": 0,
        "Refreshing": 0,
        "Adventurous": 0,
        "Classic": 0,
    }

    # High-signal coffee preference answers (always included in quiz sessions).
    preference_boosts = (
        ("satisfy my sweet tooth", {"Sweet": 6}),
        ("flavored syrup", {"Sweet": 5}),
        ("whipped cream or cold foam", {"Sweet": 4}),
        ("strong sweet tooth", {"Sweet": 6}),
        ("sweet with coffee is always welcome", {"Sweet": 4}),
        ("new desserts, pastries, and sweet creations", {"Sweet": 5, "Adventurous": 2}),
        ("wake me up and keep me focused", {"Bold": 5, "Classic": 2}),
        ("extra espresso for a stronger kick", {"Bold": 6}),
        ("nothing—i like coffee as it is", {"Bold": 3, "Classic": 4}),
        ("simple black coffee", {"Bold": 3, "Classic": 4}),
        ("refresh me and cool me down", {"Refreshing": 6}),
        ("iced coffee", {"Refreshing": 5}),
        ("comforting while i relax", {"Classic": 4, "Sweet": 1}),
        ("quiet café with a warm drink", {"Classic": 4}),
        ("surprise me with something fun", {"Adventurous": 6}),
        ("surprise me with something unique", {"Adventurous": 5}),
        ("creative seasonal menus", {"Adventurous": 5, "Sweet": 1}),
        ("specialty drinks", {"Adventurous": 3, "Sweet": 2}),
        ("rarely — i usually prefer savory", {"Bold": 2, "Classic": 3}),
        ("less sweet flavors", {"Bold": 2, "Classic": 2}),
    )
    for phrase, boosts in preference_boosts:
        if phrase in text:
            for category, points in boosts.items():
                scores[category] += points

    sweet_words = (
        "sweet",
        "vanilla",
        "caramel",
        "hazelnut",
        "syrup",
        "chocolate",
        "dessert",
        "tiramisu",
        "cinnamon",
        "pastries",
        "cheesecake",
        "brunch",
        "baking",
    )
    bold_words = (
        "strong",
        "conquer",
        "focused",
        "black coffee",
        "isn't strong",
        "black and white",
        "logic",
        "organized",
        "stronger kick",
    )
    refreshing_words = (
        "sunshine",
        "summer",
        "beach",
        "rain",
        "ice",
        "cold",
        "cool me down",
        "walk",
        "outdoor",
        "hiking",
    )
    adventurous_words = (
        "try it immediately",
        "surprise",
        "seasonal",
        "adventurous",
        "unfamiliar",
        "wander",
        "never been",
        "curiosity",
        "curious",
        "comfort zone",
        "explore",
        "fantasy",
        "wonderland",
        "pandora",
        "fun and different",
        "unique",
    )
    classic_words = (
        "peaceful",
        "quiet",
        "routine",
        "regular order",
        "calm",
        "reliable",
        "cozy",
        "stick with",
        "traditional",
        "library",
        "read",
        "comforting",
        "relax",
        "as it is",
    )

    for word in sweet_words:
        if word in text:
            scores["Sweet"] += 2
    for word in bold_words:
        if word in text:
            scores["Bold"] += 2
    for word in refreshing_words:
        if word in text:
            scores["Refreshing"] += 2
    for word in adventurous_words:
        if word in text:
            scores["Adventurous"] += 2
    for word in classic_words:
        if word in text:
            scores["Classic"] += 2

    top_category = max(scores, key=scores.get)
    if scores[top_category] == 0:
        top_category = "Classic"

    candidates = [
        drink for drink in COFFEE_DRINKS if top_category in drink["categories"]
    ]
    if not candidates:
        return random.choice(COFFEE_DRINKS)
    return random.choice(candidates)


def _inferred_traits(answers: list[dict[str, Any]]) -> dict[str, bool]:
    text = " ".join(
        f"{item.get('question', '')} {item.get('option_label', '')}".lower()
        for item in answers
    )
    return {
        "sweet": any(
            word in text
            for word in (
                "sweet",
                "syrup",
                "dessert",
                "whipped cream",
                "cold foam",
                "pastries",
                "caramel",
                "vanilla",
            )
        ),
        "bold": any(
            word in text
            for word in (
                "focused",
                "stronger kick",
                "extra espresso",
                "black coffee",
                "as it is",
                "wake me up",
            )
        ),
        "refreshing": any(
            word in text
            for word in ("cool me down", "iced", "refresh", "exploring the city")
        ),
        "adventurous": any(
            word in text
            for word in (
                "surprise",
                "fun and different",
                "unique",
                "seasonal",
                "specialty",
                "creative",
            )
        ),
        "cozy": any(
            word in text
            for word in (
                "comforting",
                "relax",
                "quiet café",
                "warm drink",
                "calm",
                "cozy",
            )
        ),
        "organized": any(
            word in text
            for word in ("to-do", "organized", "focused", "reliable", "charger")
        ),
    }


def _heuristic_blurb(drink: CoffeeDrink, answers: list[dict[str, Any]]) -> str:
    traits = _inferred_traits(answers)
    category = drink["categories"][0].lower()
    name = drink["name"]

    if traits["cozy"]:
        opener = (
            f"{name} fits a softer pace, the kind of cup you settle into when "
            "you want comfort more than spectacle."
        )
    elif traits["organized"] or traits["bold"]:
        opener = (
            f"{name} suits a clear-headed kind of energy, steady enough to keep "
            "you moving without asking for attention."
        )
    elif traits["adventurous"]:
        opener = (
            f"{name} leans playful and a little unexpected, matching a taste for "
            "something beyond the usual order."
        )
    elif traits["refreshing"]:
        opener = (
            f"{name} has an easy, cooling lift to it, made for days when you want "
            "coffee to feel light and bright."
        )
    else:
        opener = (
            f"{name} feels balanced and approachable, a cup that meets you where "
            "you are without overcomplicating the moment."
        )

    if traits["sweet"]:
        middle = (
            f"As a {category} drink, it has a gentle richness that leaves room "
            "for a flavored syrup if you want a sweeter finish."
        )
        finish = (
            "Vanilla or caramel would sit nicely beside it, soft enough to feel "
            "like a treat without hiding the coffee."
        )
    elif traits["bold"]:
        middle = (
            f"As a {category} drink, it keeps the coffee forward and unfussy, "
            "with enough presence to feel intentional."
        )
        finish = (
            "Skip the extras if you like, or keep them light so the brew stays "
            "the main character."
        )
    elif traits["adventurous"]:
        middle = (
            f"As a {category} drink, it has just enough personality to feel "
            "special while still tasting like something you would order again."
        )
        finish = (
            "It is the sort of match that rewards curiosity without turning "
            "coffee into a gimmick."
        )
    else:
        middle = (
            f"As a {category} drink, it has a simple richness that does not need "
            "dressing up to feel complete."
        )
        finish = (
            f"{name} keeps things honest and easy, just a clear, satisfying cup."
        )

    return f"{opener} {middle} {finish}"


def _soften_punctuation(text: str) -> str:
    """Prefer commas/periods over em dashes in match copy."""
    cleaned = text.replace(" — ", ", ").replace("—", ", ")
    cleaned = cleaned.replace(" – ", ", ").replace("–", ", ")
    return cleaned


def _strip_direct_answer_quotes(blurb: str, answers: list[dict[str, Any]]) -> str:
    """Remove awkward literal answer snippets if the model quoted them anyway."""
    cleaned = blurb
    for item in answers:
        label = str(item.get("option_label", "")).strip()
        if len(label) < 8:
            continue
        # Strip quoted forms of the answer text.
        for form in (label, label.lower(), label.rstrip(".")):
            cleaned = cleaned.replace(f'"{form}"', "your vibe")
            cleaned = cleaned.replace(f"“{form}”", "your vibe")
    # Clean up clumsy leftovers from replacements.
    cleaned = re.sub(r"\byour vibe\b(, your vibe)+", "your vibe", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


def _parse_ai_json(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(cleaned[start : end + 1])


def _ollama_available() -> bool:
    try:
        with httpx.Client(timeout=2.0) as client:
            response = client.get(f"{OLLAMA_BASE_URL.rstrip('/')}/api/tags")
            response.raise_for_status()
        return True
    except Exception:
        return False


def _call_ollama(prompt: str) -> str:
    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.7,
            "num_predict": 180,
        },
    }

    with httpx.Client(timeout=OLLAMA_TIMEOUT_SECONDS) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    content = data.get("response", "")
    if not content:
        raise ValueError("Empty response from Ollama")
    return content


def match_coffee_with_ai(answers: list[dict[str, Any]]) -> tuple[CoffeeDrink, str]:
    """
    Returns (drink, personalized_blurb).

    Drink selection uses a fast local heuristic so Finish never hangs.
    Ollama writes the personalized blurb when available; otherwise we fall back.
    """
    drink = _heuristic_match(answers)

    if not _ollama_available():
        logger.warning("Ollama unavailable — using heuristic blurb")
        return drink, _soften_punctuation(_heuristic_blurb(drink, answers))

    prompt = (
        "You are BrewMatch, writing like a café menu description: warm, natural, and specific.\n"
        f"The chosen drink is already decided: {drink['name']} (id: {drink['id']}).\n"
        "Write a personalized match of exactly 4 to 5 sentences.\n"
        "Match the tone of a coffee description: flowing, sensory, and human. "
        "Not salesy, not like a chatbot, and never meta.\n"
        "Avoid em dashes. Prefer commas or short separate sentences instead.\n"
        "IMPORTANT: Never quote the user's answers directly. Do not put answer text in "
        "quotation marks. Do not paste phrases like quiz options word-for-word. "
        "Paraphrase the vibe instead (for example say they like a focused morning or "
        "a comforting ritual, not the exact option text).\n"
        "Use coffee preferences (add-ons, sweetness, iced vs warm, syrups, strength) "
        "to drive the story. Personality can flavor the tone lightly.\n"
        "If they enjoy sweetness or syrups, mention a syrup pairing in one natural sentence.\n"
        "Return JSON only with keys: drink_id, personalized_match.\n"
        f"drink_id must be \"{drink['id']}\".\n\n"
        f"Drink categories: {', '.join(drink['categories'])}\n"
        f"Drink description for tone reference: {drink['description']}\n\n"
        "User answer highlights (paraphrase only, never quote):\n"
        f"{_answers_for_prompt(answers)}\n"
    )

    try:
        content = _call_ollama(prompt)
        payload = _parse_ai_json(content)
        blurb = _soften_punctuation(str(payload.get("personalized_match", "")).strip())
        blurb = _strip_direct_answer_quotes(blurb, answers)
        if not blurb:
            raise ValueError("Missing personalized_match")
        return drink, blurb
    except Exception as exc:
        logger.warning("Ollama match failed (%s) — using heuristic blurb", exc)
        return drink, _soften_punctuation(_heuristic_blurb(drink, answers))
