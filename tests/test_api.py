from fastapi.testclient import TestClient
from ..src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict_single_student():
    student_data = [{
        "student_id": 1,
        "name": "Анна",
        "attendance_rate": 95,
        "avg_grade": 85,
        "missed_assignments": 1,
        "login_frequency": 4
    }]

    response = client.post("/predict", json=student_data)
    assert response.status_code == 200

    result = response.json()
    predictions = result["predictions"]
    assert len(predictions) == 1
    assert predictions[0]["name"] == "Анна"
    assert 0.0 <= predictions[0]["dropout_risk"] <= 1.0

def test_predict_multiple_students():
    students_data = [
        {
            "student_id": 1,
            "name": "Анна",
            "attendance_rate": 95,
            "avg_grade": 85,
            "missed_assignments": 1,
            "login_frequency": 4
        },
        {
            "student_id": 2,
            "name": "Борис",
            "attendance_rate": 40,
            "avg_grade": 45,
            "missed_assignments": 8,
            "login_frequency": 1
        }
    ]

    response = client.post("/predict", json=students_data)
    assert response.status_code == 200

    result = response.json()
    predictions = result["predictions"]
    assert len(predictions) == 2
    assert predictions[0]["name"] == "Анна"
    assert predictions[1]["name"] == "Борис"
    assert all(0.0 <= p["dropout_risk"] <= 1.0 for p in predictions)

def test_predict_invalid_data():
    # Пропущено обязательное поле
    invalid_data = [{"name": "Test"}]

    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Валидация Pydantic