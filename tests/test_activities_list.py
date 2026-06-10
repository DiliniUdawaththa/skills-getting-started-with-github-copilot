"""
Tests for the GET /activities endpoint
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return all 9 activities
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Track and Field" in data
    assert "Art Studio" in data
    assert "Music Band" in data
    assert "Robotics Club" in data
    assert "Science Club" in data


def test_activities_have_required_fields(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Activity {activity_name} missing field {field}"


def test_activity_data_types(client):
    """Test that activity fields have correct data types"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        
        # All participants should be email strings
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation


def test_activities_have_participants(client):
    """Test that activities are pre-populated with participants"""
    response = client.get("/activities")
    data = response.json()
    
    # Verify specific known participants
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "emma@mergington.edu" in data["Programming Class"]["participants"]
    assert "john@mergington.edu" in data["Gym Class"]["participants"]
    assert "alex@mergington.edu" in data["Basketball Team"]["participants"]


def test_get_activities_response_format(client):
    """Test that response is a valid JSON object (dict)"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
