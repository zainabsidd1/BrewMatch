import json
import logging
import re
from typing import Any

import httpx

from coffee_catalog import COFFEE_DRINKS, CoffeeDrink, get_drink_by_id_or_name
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
        "espresso",
        "focused",
        "black coffee",
        "isn't strong",
        "black and white",
        "logic",
        "organized",
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
    return candidates[0] if candidates else COFFEE_DRINKS[0]


def _heuristic_blurb(drink: CoffeeDrink, answers: list[dict[str, Any]]) -> str:
    snippets = [item["option_label"] for item in answers if item.get("option_label")]
    primary = snippets[0] if snippets else "a slower morning"
    secondary = snippets[1] if len(snippets) > 1 else "a quiet café corner"
    likes_sweet = any(
        word in " ".join(snippets).lower()
        for word in (
            "sweet",
            "vanilla",
            "caramel",
            "hazelnut",
            "syrup",
            "chocolate",
            "dessert",
            "sweet tooth",
            "whipped cream",
            "cold foam",
            "pastries",
        )
    )

    if likes_sweet:
        finish = (
            f"A little syrup would go beautifully with {drink['name']}, "
            "rounding it out without covering up the coffee."
        )
    else:
        finish = (
            f"{drink['name']} keeps things honest and unfussy, "
            "just a clear, satisfying cup."
        )

    return (
        f"There's a calm confidence in preferring mornings that feel "
        f'"{primary.lower()}", and {drink["name"]} carries that same steady warmth. '
        f'It suits someone drawn to "{secondary.lower()}", '
        f"unhurried, grounded, and easy to return to. "
        f"As a {drink['categories'][0].lower()} drink, it has a simple richness "
        f"that doesn't need dressing up to feel complete. "
        f"{finish}"
    )


def _soften_punctuation(text: str) -> str:
    """Prefer commas/periods over em dashes in match copy."""
    cleaned = text.replace(" — ", ", ").replace("—", ", ")
    cleaned = cleaned.replace(" – ", ", ").replace("–", ", ")
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
        "Do NOT use phrases like 'curated recommendation', 'based on your quiz', "
        "'perfect for someone like you', 'next time you order', or 'random pick'.\n"
        "Weave in a few of the user's answers naturally "
        "(especially coffee job, add-ons, sweetness, iced vs warm, syrups, strength). "
        "Personality answers can flavor the tone, but coffee preferences should drive the match story.\n"
        "If they enjoy sweetness or syrups, mention a syrup pairing in one natural sentence.\n"
        "Return JSON only with keys: drink_id, personalized_match.\n"
        f"drink_id must be \"{drink['id']}\".\n\n"
        f"Drink categories: {', '.join(drink['categories'])}\n"
        f"Drink description for tone reference: {drink['description']}\n\n"
        "User answer highlights:\n"
        f"{_answers_for_prompt(answers)}\n"
    )

    try:
        content = _call_ollama(prompt)
        payload = _parse_ai_json(content)
        blurb = _soften_punctuation(str(payload.get("personalized_match", "")).strip())
        # Prefer the heuristic drink; only swap if Ollama returns a valid catalog id.
        ai_drink = get_drink_by_id_or_name(str(payload.get("drink_id", "")))
        if ai_drink:
            drink = ai_drink
        if not blurb:
            raise ValueError("Missing personalized_match")
        return drink, blurb
    except Exception as exc:
        logger.warning("Ollama match failed (%s) — using heuristic blurb", exc)
        return drink, _soften_punctuation(_heuristic_blurb(drink, answers))
