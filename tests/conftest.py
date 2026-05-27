import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def sample_activities():
    """Provide a fresh copy of activities data for each test"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team-based soccer practice and competitive matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["lily@mergington.edu", "jake@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu"]
        }
    }


@pytest.fixture
def client(sample_activities, monkeypatch):
    """Provide a TestClient with isolated activities data per test"""
    # Replace the global activities dict with our test data
    monkeypatch.setattr("src.app.activities", sample_activities)
    return TestClient(app)
