"""Tests for GET /activities endpoint"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all activities are present
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Soccer Team" in data
    assert "Art Studio" in data


def test_get_activities_response_structure(client):
    """Test that activity data has the correct structure"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    
    # Verify required fields
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Verify field types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_includes_participants(client):
    """Test that activities include their participant lists"""
    response = client.get("/activities")
    data = response.json()
    
    # Chess Club has 2 participants
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    
    # Programming Class has 2 participants
    assert len(data["Programming Class"]["participants"]) == 2
    assert "emma@mergington.edu" in data["Programming Class"]["participants"]
    assert "sophia@mergington.edu" in data["Programming Class"]["participants"]
