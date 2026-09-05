from typing import Literal, TypedDict

from coffee_catalog import COFFEE_DRINKS, CoffeeDrink

Temperature = Literal["hot", "iced"]
Sweetness = Literal["low", "medium", "high"]
Strength = Literal["mild", "medium", "bold"]
Milkiness = Literal["none", "light", "medium", "high"]

SYRUPS = ("vanilla", "caramel", "hazelnut", "chocolate")
MODIFIERS = (
    "extra shot",
    "splash of milk",
    "sweet cream",
    "cold foam",
    "whipped cream",
)

MILK_SYRUPS = ["vanilla", "caramel", "hazelnut"]
BLACK_SYRUPS = ["vanilla", "caramel"]
SWEET_SYRUPS = ["vanilla", "caramel", "chocolate"]

MILK_MODIFIERS = ["extra shot", "cold foam", "whipped cream"]
BLACK_MODIFIERS = ["splash of milk", "sweet cream", "extra shot"]


class DrinkAttributes(TypedDict):
    id: str
    name: str
    strength: Strength
    milkiness: Milkiness
    bitterness: Literal["low", "medium", "high"]
    default_sweetness: Sweetness
    temperatures: list[Temperature]
    default_temperature: Temperature
    compatible_syrups: list[str]
    compatible_modifiers: list[str]
    implied_syrup: str | None


# Base drinks used to build combinations. iced-americano maps to americano + iced.
DRINK_ATTRIBUTES: dict[str, DrinkAttributes] = {
    "americano": {
        "id": "americano",
        "name": "Americano",
        "strength": "bold",
        "milkiness": "none",
        "bitterness": "high",
        "default_sweetness": "low",
        "temperatures": ["hot", "iced"],
        "default_temperature": "hot",
        "compatible_syrups": list(BLACK_SYRUPS),
        "compatible_modifiers": list(BLACK_MODIFIERS),
        "implied_syrup": None,
    },
    "cold-brew": {
        "id": "cold-brew",
        "name": "Cold Brew",
        "strength": "medium",
        "milkiness": "none",
        "bitterness": "low",
        "default_sweetness": "low",
        "temperatures": ["iced"],
        "default_temperature": "iced",
        "compatible_syrups": list(BLACK_SYRUPS),
        "compatible_modifiers": ["sweet cream", "splash of milk", "cold foam"],
        "implied_syrup": None,
    },
    "latte": {
        "id": "latte",
        "name": "Latte",
        "strength": "mild",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "low",
        "temperatures": ["hot", "iced"],
        "default_temperature": "hot",
        "compatible_syrups": list(MILK_SYRUPS),
        "compatible_modifiers": list(MILK_MODIFIERS),
        "implied_syrup": None,
    },
    "cafe-au-lait": {
        "id": "cafe-au-lait",
        "name": "Café au Lait",
        "strength": "mild",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "low",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": list(MILK_SYRUPS),
        "compatible_modifiers": ["extra shot", "whipped cream"],
        "implied_syrup": None,
    },
    "breve": {
        "id": "breve",
        "name": "Breve",
        "strength": "medium",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "low",
        "temperatures": ["hot", "iced"],
        "default_temperature": "hot",
        "compatible_syrups": list(MILK_SYRUPS),
        "compatible_modifiers": ["extra shot", "whipped cream"],
        "implied_syrup": None,
    },
    "biscoff-latte": {
        "id": "biscoff-latte",
        "name": "Biscoff Latte",
        "strength": "mild",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "high",
        "temperatures": ["hot", "iced"],
        "default_temperature": "hot",
        "compatible_syrups": [],
        "compatible_modifiers": ["extra shot", "cold foam"],
        "implied_syrup": "biscoff",
    },
    "mocha": {
        "id": "mocha",
        "name": "Mocha",
        "strength": "medium",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "high",
        "temperatures": ["hot", "iced"],
        "default_temperature": "hot",
        "compatible_syrups": ["vanilla"],
        "compatible_modifiers": ["extra shot", "whipped cream"],
        "implied_syrup": "chocolate",
    },
    "cappuccino": {
        "id": "cappuccino",
        "name": "Cappuccino",
        "strength": "medium",
        "milkiness": "medium",
        "bitterness": "medium",
        "default_sweetness": "low",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": list(MILK_SYRUPS),
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
    "flat-white": {
        "id": "flat-white",
        "name": "Flat White",
        "strength": "medium",
        "milkiness": "medium",
        "bitterness": "medium",
        "default_sweetness": "low",
        "temperatures": ["hot", "iced"],
        "default_temperature": "hot",
        "compatible_syrups": list(MILK_SYRUPS),
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
    "cortado": {
        "id": "cortado",
        "name": "Cortado",
        "strength": "bold",
        "milkiness": "light",
        "bitterness": "medium",
        "default_sweetness": "low",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": ["vanilla"],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
    "dirty-chai": {
        "id": "dirty-chai",
        "name": "Dirty Chai",
        "strength": "medium",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "medium",
        "temperatures": ["hot", "iced"],
        "default_temperature": "hot",
        "compatible_syrups": ["vanilla"],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": "spice",
    },
    "coffee-frappe": {
        "id": "coffee-frappe",
        "name": "Coffee Frappé",
        "strength": "mild",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "high",
        "temperatures": ["iced"],
        "default_temperature": "iced",
        "compatible_syrups": list(SWEET_SYRUPS),
        "compatible_modifiers": ["whipped cream", "extra shot"],
        "implied_syrup": None,
    },
    "mazagran": {
        "id": "mazagran",
        "name": "Mazagran",
        "strength": "medium",
        "milkiness": "none",
        "bitterness": "medium",
        "default_sweetness": "medium",
        "temperatures": ["iced"],
        "default_temperature": "iced",
        "compatible_syrups": [],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
    "dalgona-coffee": {
        "id": "dalgona-coffee",
        "name": "Dalgona Coffee",
        "strength": "medium",
        "milkiness": "high",
        "bitterness": "medium",
        "default_sweetness": "medium",
        "temperatures": ["hot", "iced"],
        "default_temperature": "iced",
        "compatible_syrups": ["vanilla"],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
    "affogato": {
        "id": "affogato",
        "name": "Affogato",
        "strength": "medium",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "high",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": [],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": "vanilla",
    },
    "turkish-coffee": {
        "id": "turkish-coffee",
        "name": "Turkish Coffee",
        "strength": "bold",
        "milkiness": "none",
        "bitterness": "high",
        "default_sweetness": "low",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": [],
        "compatible_modifiers": [],
        "implied_syrup": None,
    },
    "arabic-coffee": {
        "id": "arabic-coffee",
        "name": "Arabic Coffee",
        "strength": "bold",
        "milkiness": "none",
        "bitterness": "medium",
        "default_sweetness": "low",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": [],
        "compatible_modifiers": [],
        "implied_syrup": "spice",
    },
    "cuban-coffee": {
        "id": "cuban-coffee",
        "name": "Cuban Coffee",
        "strength": "bold",
        "milkiness": "none",
        "bitterness": "medium",
        "default_sweetness": "high",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": [],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
    "espresso-con-panna": {
        "id": "espresso-con-panna",
        "name": "Espresso Con Panna",
        "strength": "bold",
        "milkiness": "light",
        "bitterness": "high",
        "default_sweetness": "medium",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": ["vanilla", "caramel"],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
    "vienna-coffee": {
        "id": "vienna-coffee",
        "name": "Vienna Coffee",
        "strength": "medium",
        "milkiness": "high",
        "bitterness": "low",
        "default_sweetness": "medium",
        "temperatures": ["hot"],
        "default_temperature": "hot",
        "compatible_syrups": ["vanilla", "caramel"],
        "compatible_modifiers": ["extra shot"],
        "implied_syrup": None,
    },
}

# Quiz catalog drinks that are temperature variants of a base.
ALIASES: dict[str, tuple[str, Temperature]] = {
    "iced-americano": ("americano", "iced"),
}


def catalog_logging_options() -> list[dict[str, object]]:
    options: list[dict[str, object]] = []
    for drink in COFFEE_DRINKS:
        if drink["id"] in ALIASES:
            base_id, temperature = ALIASES[drink["id"]]
            attrs = DRINK_ATTRIBUTES[base_id]
            options.append(
                {
                    "id": drink["id"],
                    "name": drink["name"],
                    "temperatures": [temperature],
                    "compatible_syrups": list(attrs["compatible_syrups"]),
                }
            )
            continue
        attrs = DRINK_ATTRIBUTES[drink["id"]]
        options.append(
            {
                "id": drink["id"],
                "name": drink["name"],
                "temperatures": list(attrs["temperatures"]),
                "compatible_syrups": list(attrs["compatible_syrups"]),
            }
        )
    return options


def resolve_logged_drink(drink_id: str, drink_name: str) -> tuple[str, DrinkAttributes]:
    key = drink_id.strip().lower()
    if key in ALIASES:
        base_id, _temp = ALIASES[key]
        return base_id, DRINK_ATTRIBUTES[base_id]
    if key in DRINK_ATTRIBUTES:
        return key, DRINK_ATTRIBUTES[key]
    name_key = drink_name.strip().lower()
    for attrs in DRINK_ATTRIBUTES.values():
        if attrs["name"].lower() == name_key:
            return attrs["id"], attrs
    catalog: CoffeeDrink | None = next(
        (d for d in COFFEE_DRINKS if d["id"] == key or d["name"].lower() == name_key),
        None,
    )
    if catalog and catalog["id"] in DRINK_ATTRIBUTES:
        return catalog["id"], DRINK_ATTRIBUTES[catalog["id"]]
    if catalog and catalog["id"] in ALIASES:
        base_id, _temp = ALIASES[catalog["id"]]
        return base_id, DRINK_ATTRIBUTES[base_id]
    return "latte", DRINK_ATTRIBUTES["latte"]


def logged_temperature(drink_id: str, drink_name: str, attrs: DrinkAttributes) -> Temperature | None:
    key = drink_id.strip().lower()
    name = drink_name.strip().lower()

    if key in ALIASES:
        return ALIASES[key][1]
    if key.startswith("iced-") or name.startswith("iced "):
        return "iced"
    if name.startswith("hot "):
        return "hot"

    temps = attrs["temperatures"]
    if temps == ["iced"]:
        return "iced"
    if temps == ["hot"]:
        return "hot"
    return None
