import pytest
from src.app import activities


def test_signup_for_activity(client, fresh_activities, monkeypatch):
    """Test POST /activities/{activity_name}/signup successfully adds participant"""
    # Replace the global activities with fresh test data
    monkeypatch.setattr("src.app.activities", fresh_activities)

    # Sign up a new student for Chess Club
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]

    # Verify the participant was added
    get_response = client.get("/activities")
    activities_data = get_response.json()
    chess_club = activities_data["Chess Club"]
    assert "newstudent@mergington.edu" in chess_club["participants"]
    assert len(chess_club["participants"]) == 3  # Original 2 + 1 new


def test_signup_for_nonexistent_activity(client, fresh_activities, monkeypatch):
    """Test POST /activities/{activity_name}/signup fails for non-existent activity"""
    # Replace the global activities with fresh test data
    monkeypatch.setattr("src.app.activities", fresh_activities)

    response = client.post("/activities/NonExistent%20Activity/signup?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]