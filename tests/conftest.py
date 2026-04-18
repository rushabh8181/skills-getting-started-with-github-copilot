import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Fixture for FastAPI TestClient."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activities before each test for isolation."""
    # Import the activities dict from app
    from src.app import activities
    # Reset participants for all activities
    for activity in activities.values():
        activity['participants'] = []
    yield
    # No teardown needed for in-memory reset
