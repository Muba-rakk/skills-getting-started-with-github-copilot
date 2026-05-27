"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


def test_signup_new_participant_success(client):
    """Test successful signup for a new participant"""
    response = client.post(
        "/activities/Chess Club/signup?email=newemail@mergington.edu",
        params={"email": "newemail@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newemail@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that participant is actually added to activity after signup"""
    client.post(
        "/activities/Soccer Team/signup?email=newstudent@mergington.edu",
        params={"email": "newstudent@mergington.edu"}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "newstudent@mergington.edu" in activities["Soccer Team"]["participants"]


def test_signup_duplicate_email_returns_error(client):
    """Test that signup fails when participant is already signed up"""
    # Try to sign up someone already registered for Chess Club
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signup fails for non-existent activity"""
    response = client.post(
        "/activities/Fake Activity/signup?email=student@mergington.edu",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_with_multiple_participants(client):
    """Test multiple different participants can signup for same activity"""
    # Sign up first participant
    response1 = client.post(
        "/activities/Art Studio/signup?email=user1@mergington.edu",
        params={"email": "user1@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Sign up second participant
    response2 = client.post(
        "/activities/Art Studio/signup?email=user2@mergington.edu",
        params={"email": "user2@mergington.edu"}
    )
    assert response2.status_code == 200
    
    # Verify both were added
    response = client.get("/activities")
    participants = response.json()["Art Studio"]["participants"]
    assert "user1@mergington.edu" in participants
    assert "user2@mergington.edu" in participants


def test_signup_respects_max_participants(client):
    """Test that signup works up to max_participants limit"""
    # Art Studio has max 16 participants and currently has 1
    # So we should be able to add more
    response = client.post(
        "/activities/Art Studio/signup?email=test@mergington.edu",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 200
    
    # Verify participant count increases
    activities_response = client.get("/activities")
    art_studio = activities_response.json()["Art Studio"]
    assert len(art_studio["participants"]) == 2  # ava + test
