"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""
import pytest


def test_signup_new_student_success(client, test_emails):
    """Test successful signup of a new student to an activity"""
    new_email = test_emails["new_student"]
    activity_name = "Chess Club"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {new_email} for {activity_name}"
    
    # Verify the student was actually added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert new_email in activities_data[activity_name]["participants"]


def test_signup_multiple_students_different_activities(client, test_emails):
    """Test that multiple students can sign up for different activities"""
    email1 = test_emails["new_student"]
    email2 = "another_new@mergington.edu"
    
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email1}
    )
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email2}
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both signups worked
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email1 in activities_data["Chess Club"]["participants"]
    assert email2 in activities_data["Programming Class"]["participants"]


def test_signup_same_student_multiple_activities(client, test_emails):
    """Test that a student can sign up for multiple different activities"""
    email = test_emails["new_student"]
    
    response1 = client.post("/activities/Chess Club/signup", params={"email": email})
    response2 = client.post("/activities/Art Studio/signup", params={"email": email})
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both signups worked
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data["Chess Club"]["participants"]
    assert email in activities_data["Art Studio"]["participants"]


def test_signup_nonexistent_activity_returns_404(client, test_emails):
    """Test that signing up for a non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": test_emails["new_student"]}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_already_enrolled_returns_400(client, test_emails):
    """Test that signing up twice for the same activity returns 400"""
    email = test_emails["existing"]  # michael@mergington.edu (already in Chess Club)
    
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up"


def test_signup_preserves_existing_participants(client, test_emails):
    """Test that signup doesn't remove existing participants"""
    activity_name = "Chess Club"
    new_email = test_emails["new_student"]
    
    # Get original participants
    response_before = client.get("/activities")
    original_participants = response_before.json()[activity_name]["participants"].copy()
    
    # Sign up new student
    client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    
    # Check that original participants are still there
    response_after = client.get("/activities")
    new_participants = response_after.json()[activity_name]["participants"]
    
    for original_participant in original_participants:
        assert original_participant in new_participants


def test_signup_response_message_format(client, test_emails):
    """Test that signup response message is properly formatted"""
    email = test_emails["new_student"]
    activity = "Music Band"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_case_sensitive_activity_name(client, test_emails):
    """Test that activity names are case-sensitive"""
    response = client.post(
        "/activities/chess club/signup",  # lowercase
        params={"email": test_emails["new_student"]}
    )
    
    assert response.status_code == 404


def test_signup_with_special_characters_email(client):
    """Test signup with valid email containing special characters"""
    email_with_plus = "student+extra@mergington.edu"
    activity = "Robotics Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email_with_plus}
    )
    
    assert response.status_code == 200
    
    # Verify it was added
    activities_response = client.get("/activities")
    assert email_with_plus in activities_response.json()[activity]["participants"]
