from typing import TypedDict


class CoffeeDrink(TypedDict):
    id: str
    name: str
    description: str
    categories: list[str]


COFFEE_DRINKS: list[CoffeeDrink] = [
    {
        "id": "espresso",
        "name": "Espresso",
        "description": (
            "A rich, concentrated shot of coffee with an intense aroma and bold flavor. "
            "Served in a small cup, it's the foundation of many classic espresso-based drinks "
            "and is perfect for those who enjoy coffee in its purest form."
        ),
        "categories": ["Classic", "Bold"],
    },
    {
        "id": "americano",
        "name": "Americano",
        "description": (
            "A smooth black coffee made by combining espresso with hot water. "
            "It has the richness of espresso with a lighter body, making it ideal for those "
            "who enjoy a strong yet easy-to-drink coffee."
        ),
        "categories": ["Classic"],
    },
    {
        "id": "iced-americano",
        "name": "Iced Americano",
        "description": (
            "A refreshing version of the Americano, made with espresso, cold water, and ice. "
            "Crisp, bold, and low in sweetness, it's a favorite for warm days."
        ),
        "categories": ["Classic", "Refreshing"],
    },
    {
        "id": "cold-brew",
        "name": "Cold Brew",
        "description": (
            "Made by steeping coffee grounds in cold water for many hours, Cold Brew is "
            "naturally smooth, mellow, and less acidic than traditional iced coffee, "
            "with a subtle sweetness."
        ),
        "categories": ["Refreshing"],
    },
    {
        "id": "latte",
        "name": "Latte",
        "description": (
            "A creamy coffee made with espresso and steamed milk, finished with a light "
            "layer of foam. Mild, comforting, and highly customizable with flavored syrups."
        ),
        "categories": ["Classic"],
    },
    {
        "id": "biscoff-latte",
        "name": "Biscoff Latte",
        "description": (
            "A smooth latte blended with the caramelized, spiced flavor of Biscoff cookies. "
            "Creamy, comforting, and slightly sweet, it's perfect for anyone who enjoys "
            "dessert-inspired coffee."
        ),
        "categories": ["Sweet"],
    },
    {
        "id": "mocha",
        "name": "Mocha",
        "description": (
            "A rich blend of espresso, steamed milk, and chocolate. Combining the boldness "
            "of coffee with the sweetness of cocoa, it's a classic choice for chocolate lovers."
        ),
        "categories": ["Sweet"],
    },
    {
        "id": "cappuccino",
        "name": "Cappuccino",
        "description": (
            "A balanced espresso drink made with equal parts espresso, steamed milk, and "
            "velvety milk foam. Light, airy, and satisfying without being overly sweet."
        ),
        "categories": ["Classic"],
    },
    {
        "id": "flat-white",
        "name": "Flat White",
        "description": (
            "A velvety coffee made with espresso and finely steamed milk. It has a stronger "
            "coffee flavor than a latte while maintaining a silky, smooth texture."
        ),
        "categories": ["Classic"],
    },
    {
        "id": "cortado",
        "name": "Cortado",
        "description": (
            "A bold espresso drink balanced with a small amount of steamed milk to reduce "
            "acidity while preserving the coffee's rich flavor. Ideal for those who enjoy "
            "a stronger cup without too much milk."
        ),
        "categories": ["Classic", "Bold"],
    },
    {
        "id": "dirty-chai",
        "name": "Dirty Chai",
        "description": (
            "A comforting combination of spicy chai tea and espresso, blended with steamed milk. "
            "The warm spices complement the coffee, creating a unique and flavorful drink."
        ),
        "categories": ["Adventurous"],
    },
    {
        "id": "coffee-frappe",
        "name": "Coffee Frappé",
        "description": (
            "A blended iced coffee made with coffee, ice, and milk for a smooth, frosty texture. "
            "Sweet, refreshing, and perfect as a coffee treat on a hot day."
        ),
        "categories": ["Sweet", "Refreshing"],
    },
    {
        "id": "dalgona-coffee",
        "name": "Dalgona Coffee",
        "description": (
            "A visually striking whipped coffee made by beating instant coffee, sugar, and hot "
            "water into a thick, fluffy foam before layering it over cold or hot milk. Light, "
            "creamy, and perfect for anyone who enjoys trying viral coffee trends."
        ),
        "categories": ["Adventurous"],
    },
    {
        "id": "affogato",
        "name": "Affogato",
        "description": (
            'A coffee dessert featuring a scoop of vanilla gelato or ice cream "drowned" with '
            "a shot of hot espresso. The contrast of hot and cold makes for a simple yet "
            "indulgent treat."
        ),
        "categories": ["Sweet"],
    },
    {
        "id": "turkish-coffee",
        "name": "Turkish Coffee",
        "description": (
            "A traditional unfiltered coffee brewed from finely ground beans in a small pot "
            "called a cezve. Thick, aromatic, and deeply flavorful, it's often enjoyed slowly "
            "and sometimes served with Turkish delight."
        ),
        "categories": ["Bold", "Adventurous"],
    },
    {
        "id": "vienna-coffee",
        "name": "Vienna Coffee",
        "description": (
            "A luxurious drink made with a double shot of espresso topped with a generous "
            "layer of freshly whipped cream instead of steamed milk. Rich, creamy, and "
            "perfect for those who enjoy a decadent coffee experience."
        ),
        "categories": ["Sweet"],
    },
]


DRINKS_BY_ID = {drink["id"]: drink for drink in COFFEE_DRINKS}
DRINKS_BY_NAME = {drink["name"].lower(): drink for drink in COFFEE_DRINKS}


def get_drink_by_id_or_name(value: str) -> CoffeeDrink | None:
    key = value.strip().lower()
    return DRINKS_BY_ID.get(key) or DRINKS_BY_NAME.get(key)
