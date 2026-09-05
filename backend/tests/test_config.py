from config import cors_origins


def test_cors_defaults_to_local_frontend():
    assert cors_origins() == ["http://localhost:3000"]
