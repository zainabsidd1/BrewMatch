from typing import TypedDict


class CoffeeDrink(TypedDict):
    id: str
    name: str
    description: str
    categories: list[str]


COFFEE_DRINKS: list[CoffeeDrink] = [
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
            "Unlike iced coffee that cools a hot brew with ice, Cold Brew is made by steeping "
            "coffee grounds in cold water for at least 12 hours. The slow brew keeps acidity low "
            "and the flavor concentrated, with a smooth mouthfeel that isn't watered down by extra ice."
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
        "id": "cafe-au-lait",
        "name": "Café au Lait",
        "description": (
            "Café au lait, or coffee with milk, uses equal parts freshly brewed coffee and hot milk "
            "instead of espresso. Often made with a French press, it is a smooth, mild blend for "
            "anyone who likes coffee simple but effective."
        ),
        "categories": ["Classic"],
    },
    {
        "id": "breve",
        "name": "Breve",
        "description": (
            "A rich espresso drink made with equal parts espresso and steamed half-and-half. "
            "Typically served in a small cup, it can be enjoyed hot or poured over ice, with a "
            "creamy, heavier texture than a standard latte."
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
        "id": "mazagran",
        "name": "Mazagran",
        "description": (
            "An iced coffee mixed with coffee or a double espresso, fresh lemon juice, sugar, and ice. "
            "Bright and citrusy, it is a refreshing alternative to hot coffee in warmer weather."
        ),
        "categories": ["Refreshing", "Adventurous"],
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
            "A hot coffee brewed from finely ground beans in a copper pot called a cezve "
            "(pronounced jehz-veh) on the stovetop. It is unfiltered and can be served with "
            "or without sugar, with a thick texture and rich flavor."
        ),
        "categories": ["Bold", "Adventurous"],
    },
    {
        "id": "arabic-coffee",
        "name": "Arabic Coffee",
        "description": (
            "Known in Arabic as qahwa, this is a family of brewed coffees made from Arabica beans. "
            "Preparations vary across the Middle East. It is often spiced with cardamom, and can "
            "also be served plain or with sugar."
        ),
        "categories": ["Bold", "Adventurous"],
    },
    {
        "id": "cuban-coffee",
        "name": "Cuban Coffee",
        "description": (
            "Also known as cafecito or café cubano, this is a sweetened espresso typically brewed "
            "from finely ground beans in a moka pot and poured over espuma, a froth whipped from "
            "espresso and sugar. Served in small cups, it can be enjoyed throughout the day."
        ),
        "categories": ["Sweet", "Bold"],
    },
    {
        "id": "espresso-con-panna",
        "name": "Espresso Con Panna",
        "description": (
            "A single or double shot of espresso topped with whipped cream. The contrast of "
            "bold espresso and the sweetness of the cream makes a strong, dessert-like coffee."
        ),
        "categories": ["Sweet", "Bold"],
    },
    {
        "id": "vienna-coffee",
        "name": "Vienna Coffee",
        "description": (
            "A double espresso topped with whisked whipped cream instead of steamed milk, then "
            "dusted with cocoa powder or chocolate shavings. Rich, creamy, and a decadent treat "
            "for anyone who likes a dessert-like coffee."
        ),
        "categories": ["Sweet"],
    },
]


DRINKS_BY_ID = {drink["id"]: drink for drink in COFFEE_DRINKS}
DRINKS_BY_NAME = {drink["name"].lower(): drink for drink in COFFEE_DRINKS}
DRINKS_BY_NAME.update(
    {
        "cafe au lait": DRINKS_BY_ID["cafe-au-lait"],
        "café au lait": DRINKS_BY_ID["cafe-au-lait"],
        "cafecito": DRINKS_BY_ID["cuban-coffee"],
        "café cubano": DRINKS_BY_ID["cuban-coffee"],
        "qahwa": DRINKS_BY_ID["arabic-coffee"],
        "espresso con panna": DRINKS_BY_ID["espresso-con-panna"],
    }
)


def get_drink_by_id_or_name(value: str) -> CoffeeDrink | None:
    key = value.strip().lower()
    return DRINKS_BY_ID.get(key) or DRINKS_BY_NAME.get(key)
