from config import cors_origin_regex, cors_origins


def test_cors_defaults_to_local_frontend():
    assert cors_origins() == [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]


def test_cors_origin_regex_allows_vercel_previews():
    assert cors_origin_regex() == r"https://([a-z0-9-]+\.)*vercel\.app"
