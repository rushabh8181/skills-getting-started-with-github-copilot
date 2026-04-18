import pytest
from fastapi.testclient import TestClient

# Arrange-Act-Assert (AAA) pattern is used for all tests

def test_root_redirect(client):
    # Arrange: client fixture provided
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307
    assert "text/html" in response.headers["content-type"]
    assert b"High School Activities" in response.content

def test_get_activities(client):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for name, activity in data.items():
        assert isinstance(name, str)
        assert isinstance(activity, dict)
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

@pytest.mark.parametrize("activity_name,email", [("Chess Club", "alice@example.com")])
def test_signup_success(client, activity_name, email):
    # Arrange
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    expected = f"Signed up {email} for {activity_name}"
    assert response.json()["message"] == expected

@pytest.mark.parametrize("activity_name,email", [("Nonexistent", "bob@example.com")])
def test_signup_activity_not_found(client, activity_name, email):
    # Arrange
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.parametrize("activity_name,email", [("Chess Club", "alice@example.com")])
def test_signup_duplicate(client, activity_name, email):
    # Arrange
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

@pytest.mark.parametrize("activity_name,email", [("Chess Club", "eve@example.com")])
def test_unregister_success(client, activity_name, email):
    # Arrange
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    expected = f"Removed {email} from {activity_name}"
    assert response.json()["message"] == expected

@pytest.mark.parametrize("activity_name,email", [("Nonexistent", "bob@example.com")])
def test_unregister_activity_not_found(client, activity_name, email):
    # Arrange
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.parametrize("activity_name,email", [("Chess Club", "ghost@example.com")])
def test_unregister_not_signed_up(client, activity_name, email):
    # Arrange
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()
