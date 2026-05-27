"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

import pytest


def test_delete_participant_success(client):
    """Test successful deletion of a participant"""
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_delete_removes_participant_from_activity(client):
    """Test that participant is actually removed after deletion"""
    client.delete(
        "/activities/Programming Class/participants/emma@mergington.edu"
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "emma@mergington.edu" not in activities["Programming Class"]["participants"]
    # But the other participant should still be there
    assert "sophia@mergington.edu" in activities["Programming Class"]["participants"]


def test_delete_nonexistent_participant_returns_404(client):
    """Test that deleting non-existent participant returns 404"""
    response = client.delete(
        "/activities/Chess Club/participants/nonexistent@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_delete_participant_from_nonexistent_activity_returns_404(client):
    """Test that deleting from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent Activity/participants/someone@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_delete_multiple_participants(client):
    """Test deleting multiple different participants from an activity"""
    # Soccer Team has lily and jake
    response1 = client.delete(
        "/activities/Soccer Team/participants/lily@mergington.edu"
    )
    assert response1.status_code == 200
    
    response2 = client.delete(
        "/activities/Soccer Team/participants/jake@mergington.edu"
    )
    assert response2.status_code == 200
    
    # Verify both were removed
    response = client.get("/activities")
    soccer_team = response.json()["Soccer Team"]
    assert "lily@mergington.edu" not in soccer_team["participants"]
    assert "jake@mergington.edu" not in soccer_team["participants"]
    assert len(soccer_team["participants"]) == 0


def test_delete_then_signup_same_activity(client):
    """Test signup workflow after deleting a participant"""
    # First, delete a participant
    client.delete(
        "/activities/Art Studio/participants/ava@mergington.edu"
    )
    
    # Then sign up a new participant
    client.post(
        "/activities/Art Studio/signup?email=newperson@mergington.edu",
        params={"email": "newperson@mergington.edu"}
    )
    
    # Verify the changes
    response = client.get("/activities")
    art_studio = response.json()["Art Studio"]
    assert "ava@mergington.edu" not in art_studio["participants"]
    assert "newperson@mergington.edu" in art_studio["participants"]
