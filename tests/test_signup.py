"""Tests for POST /activities/{activity_name}/signup endpoint"""


def test_signup_new_participant_success(client):
    """Test successful signup for a new participant"""
    # Arrange
    email = "newemail@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that participant is actually added to activity after signup"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Soccer Team"
    
    # Act
    client.post(
        f"/activities/{activity}/signup?email={email}",
        params={"email": email}
    )
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert email in activities[activity]["participants"]


def test_signup_duplicate_email_returns_error(client):
    """Test that signup fails when participant is already signed up"""
    # Arrange
    duplicate_email = "michael@mergington.edu"
    activity = "Chess Club"
    expected_status = 400
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={duplicate_email}",
        params={"email": duplicate_email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == expected_status
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signup fails for non-existent activity"""
    # Arrange
    email = "student@mergington.edu"
    activity = "Fake Activity"
    expected_status = 404
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == expected_status
    assert "not found" in data["detail"].lower()


def test_signup_with_multiple_participants(client):
    """Test multiple different participants can signup for same activity"""
    # Arrange
    emails = ["user1@mergington.edu", "user2@mergington.edu"]
    activity = "Art Studio"
    
    # Act
    for email in emails:
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    for email in emails:
        assert email in participants


def test_signup_respects_max_participants(client):
    """Test that signup works up to max_participants limit"""
    # Arrange
    email = "test@mergington.edu"
    activity = "Art Studio"
    expected_count = 2  # ava (initial) + test (new)
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    art_studio = activities_response.json()[activity]
    
    # Assert
    assert response.status_code == 200
    assert len(art_studio["participants"]) == expected_count
