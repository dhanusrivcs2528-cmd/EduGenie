from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["application"] == "EduGenie"


def test_qa_validation():
    response = client.post(
        "/qa",
        json={
            "question": ""
        },
    )

    assert response.status_code == 422


def test_explain_validation():
    response = client.post(
        "/explain",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422


def test_quiz_validation():
    response = client.post(
        "/quiz",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422


def test_summary_validation():
    response = client.post(
        "/summarize",
        json={
            "text": ""
        },
    )

    assert response.status_code == 422


def test_learning_path_validation():
    response = client.post(
        "/learn/recommendations",
        json={
            "topic": ""
        },
    )

    assert response.status_code == 422