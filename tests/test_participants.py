"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""


def test_delete_participant_success(client):
    """Test successful deletion of a participant"""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_delete_removes_participant_from_activity(client):
    """Test that participant is actually removed after deletion"""
    # Arrange
    email_to_remove = "emma@mergington.edu"
    email_to_keep = "sophia@mergington.edu"
    activity = "Programming Class"
    
    # Act
    client.delete(
        f"/activities/{activity}/participants/{email_to_remove}"
    )
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert email_to_remove not in activities[activity]["participants"]
    assert email_to_keep in activities[activity]["participants"]


def test_delete_nonexistent_participant_returns_404(client):
    """Test that deleting non-existent participant returns 404"""
    # Arrange
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"
    expected_status = 404
    
    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    data = response.json()
    
    # Assert
    assert response.status_code == expected_status
    assert "not found" in data["detail"].lower()


def test_delete_participant_from_nonexistent_activity_returns_404(client):
    """Test that deleting from non-existent activity returns 404"""
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Activity"
    expected_status = 404
    
    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    data = response.json()
    
    # Assert
    assert response.status_code == expected_status
    assert "not found" in data["detail"].lower()


def test_delete_multiple_participants(client):
    """Test deleting multiple different participants from an activity"""
    # Arrange
    emails_to_delete = ["lily@mergington.edu", "jake@mergington.edu"]
    activity = "Soccer Team"
    
    # Act
    for email in emails_to_delete:
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response.status_code == 200
    
    # Assert
    response = client.get("/activities")
    soccer_team = response.json()[activity]
    for email in emails_to_delete:
        assert email not in soccer_team["participants"]
    assert len(soccer_team["participants"]) == 0


def test_delete_then_signup_same_activity(client):
    """Test signup workflow after deleting a participant"""
    # Arrange
    email_to_delete = "ava@mergington.edu"
    email_to_add = "newperson@mergington.edu"
    activity = "Art Studio"
    
    # Act
    client.delete(
        f"/activities/{activity}/participants/{email_to_delete}"
    )
    client.post(
        f"/activities/{activity}/signup?email={email_to_add}",
        params={"email": email_to_add}
    )
    response = client.get("/activities")
    art_studio = response.json()[activity]
    
    # Assert
    assert email_to_delete not in art_studio["participants"]
    assert email_to_add in art_studio["participants"]
