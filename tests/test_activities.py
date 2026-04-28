import pytest
from src.app import activities


def test_get_activities(client, fresh_activities, monkeypatch):
    """Test GET /activities returns all activities"""
    # Replace the global activities with fresh test data
    monkeypatch.setattr("src.app.activities", fresh_activities)

    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    # Check that we get all activities
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) == 2