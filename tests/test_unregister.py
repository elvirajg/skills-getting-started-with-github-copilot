import pytest
from src.app import activities


def test_unregister_from_activity(client, fresh_activities, monkeypatch):
    """Test DELETE /activities/{activity_name}/unregister successfully removes participant"""
    # Replace the global activities with fresh test data
    monkeypatch.setattr("src.app.activities", fresh_activities)

    # Unregister an existing student from Chess Club
    response = client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered michael@mergington.edu from Chess Club" in data["message"]

    # Verify the participant was removed
    get_response = client.get("/activities")
    activities_data = get_response.json()
    chess_club = activities_data["Chess Club"]
    assert "michael@mergington.edu" not in chess_club["participants"]
    assert len(chess_club["participants"]) == 1  # Original 2 - 1 removed


def test_unregister_from_nonexistent_activity(client, fresh_activities, monkeypatch):
    """Test DELETE /activities/{activity_name}/unregister fails for non-existent activity"""
    # Replace the global activities with fresh test data
    monkeypatch.setattr("src.app.activities", fresh_activities)

    response = client.delete("/activities/NonExistent%20Activity/unregister?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_non_registered_student(client, fresh_activities, monkeypatch):
    """Test DELETE /activities/{activity_name}/unregister fails for student not registered"""
    # Replace the global activities with fresh test data
    monkeypatch.setattr("src.app.activities", fresh_activities)

    response = client.delete("/activities/Chess%20Club/unregister?email=notregistered@mergington.edu")

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is not registered for this activity" in data["detail"]