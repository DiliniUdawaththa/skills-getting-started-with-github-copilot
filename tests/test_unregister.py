"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint
"""
import pytest


def test_unregister_existing_participant_success(client, test_emails):
    """Test successful unregistration of an existing participant"""
    email = test_emails["existing"]  # michael@mergington.edu (in Chess Club)
    activity_name = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify they were actually removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_preserves_other_participants(client, test_emails):
    """Test that unregistration doesn't affect other participants"""
    email_to_remove = test_emails["existing"]  # michael@mergington.edu
    activity_name = "Chess Club"
    
    # Get original participant list
    response_before = client.get("/activities")
    original_participants = response_before.json()[activity_name]["participants"].copy()
    
    # Remove one participant
    client.delete(f"/activities/{activity_name}/participants/{email_to_remove}")
    
    # Check others are still there
    response_after = client.get("/activities")
    remaining_participants = response_after.json()[activity_name]["participants"]
    
    for participant in original_participants:
        if participant != email_to_remove:
            assert participant in remaining_participants


def test_unregister_nonexistent_activity_returns_404(client, test_emails):
    """Test that unregistering from non-existent activity returns 404"""
    response = client.delete(
        f"/activities/Fake Club/participants/{test_emails['existing']}"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_not_enrolled_returns_404(client, test_emails):
    """Test that unregistering a non-participant returns 404"""
    email = test_emails["unregistered"]  # nobody@mergington.edu
    activity_name = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Participant not found"


def test_unregister_twice_returns_404(client, test_emails):
    """Test that unregistering the same person twice returns 404 on second attempt"""
    email = test_emails["existing"]
    activity_name = "Chess Club"
    
    # First unregister should succeed
    response1 = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert response2.status_code == 404
    assert response2.json()["detail"] == "Participant not found"


def test_unregister_multiple_participants_sequentially(client):
    """Test unregistering multiple participants from the same activity"""
    activity_name = "Chess Club"
    email1 = "michael@mergington.edu"
    email2 = "daniel@mergington.edu"
    
    # Unregister first participant
    response1 = client.delete(
        f"/activities/{activity_name}/participants/{email1}"
    )
    assert response1.status_code == 200
    
    # Unregister second participant
    response2 = client.delete(
        f"/activities/{activity_name}/participants/{email2}"
    )
    assert response2.status_code == 200
    
    # Verify both are gone
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email1 not in participants
    assert email2 not in participants


def test_unregister_case_sensitive_activity_name(client, test_emails):
    """Test that activity names are case-sensitive in unregister"""
    response = client.delete(
        f"/activities/chess club/participants/{test_emails['existing']}"  # lowercase
    )
    
    assert response.status_code == 404


def test_unregister_case_sensitive_email(client):
    """Test email matching in unregister"""
    activity_name = "Chess Club"
    email_lowercase = "michael@mergington.edu"
    
    # Try to unregister with different case - should fail if email is case-sensitive
    response = client.delete(
        f"/activities/{activity_name}/participants/MICHAEL@MERGINGTON.EDU"
    )
    
    # This tests the actual behavior - depending on implementation
    # If emails are case-insensitive in the system, this would succeed
    # If case-sensitive, it should return 404
    # The current implementation likely treats them case-sensitively
    assert response.status_code == 404


def test_unregister_response_message_format(client, test_emails):
    """Test that unregister response message is properly formatted"""
    email = test_emails["existing"]
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_unregister_via_signup_then_unregister(client, test_emails):
    """Test the full cycle: signup, then unregister"""
    email = test_emails["new_student"]
    activity = "Science Club"
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Verify signup
    activities_before = client.get("/activities").json()
    assert email in activities_before[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify removal
    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity]["participants"]
