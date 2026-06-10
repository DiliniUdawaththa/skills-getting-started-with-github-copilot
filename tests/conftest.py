"""
Pytest configuration and shared fixtures for FastAPI app tests
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def fresh_activities():
    """
    Fixture that provides a fresh copy of the activities dictionary
    Resets the app's activities to this fresh state before each test
    """
    original_activities = {
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
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for interschool tournaments",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Track and Field": {
            "description": "Sprint, distance, and field event training",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["james@mergington.edu", "nina@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture exploration",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn and perform instrumental music",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["zoe@mergington.edu", "rachel@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for competitions",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["charles@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore STEM topics",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["isabella@mergington.edu", "thomas@mergington.edu"]
        }
    }
    
    # Reset the app's activities to the original state before each test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
    
    yield activities
    
    # Clean up: reset after test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def client(fresh_activities):
    """
    Fixture that provides a TestClient for the FastAPI app
    Depends on fresh_activities to ensure clean state
    """
    return TestClient(app)


@pytest.fixture
def test_emails():
    """
    Fixture providing sample test email addresses
    """
    return {
        "new_student": "newstudent@mergington.edu",
        "existing": "michael@mergington.edu",
        "another_existing": "emma@mergington.edu",
        "unregistered": "nobody@mergington.edu"
    }
