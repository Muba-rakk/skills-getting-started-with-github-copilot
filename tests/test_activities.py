"""Tests for GET /activities endpoint"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Soccer Team", "Art Studio"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activities_response_structure(client):
    """Test that activity data has the correct structure"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    expected_types = {
        "description": str,
        "schedule": str,
        "max_participants": int,
        "participants": list
    }
    
    # Act
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    # Assert
    for field in required_fields:
        assert field in activity
    for field, expected_type in expected_types.items():
        assert isinstance(activity[field], expected_type)


def test_get_activities_includes_participants(client):
    """Test that activities include their participant lists"""
    # Arrange
    chess_club_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    programming_participants = ["emma@mergington.edu", "sophia@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert len(data["Chess Club"]["participants"]) == 2
    for participant in chess_club_participants:
        assert participant in data["Chess Club"]["participants"]
    
    assert len(data["Programming Class"]["participants"]) == 2
    for participant in programming_participants:
        assert participant in data["Programming Class"]["participants"]
