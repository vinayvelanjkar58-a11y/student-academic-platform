from app import create_app


def setup_client():
    app = create_app()
    return app.test_client()


def test_home():
    client = setup_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_health():
    client = setup_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_create_student():
    client = setup_client()
    response = client.post(
        "/students",
        json={"name": "Asha", "email": "asha@example.com"}
    )
    assert response.status_code == 201
    assert response.json["name"] == "Asha"


def test_create_course():
    client = setup_client()
    response = client.post(
        "/courses",
        json={"name": "Python", "credits": 3}
    )
    assert response.status_code == 201


def test_course_rejects_more_than_18_credits():
    client = setup_client()
    response = client.post(
        "/courses",
        json={"name": "Invalid Course", "credits": 19}
    )
    assert response.status_code == 400


def test_enrollment_and_duplicate():
    client = setup_client()
    student = client.post(
        "/students",
        json={"name": "Ravi", "email": "ravi@example.com"}
    ).json
    course = client.post(
        "/courses",
        json={"name": "Maths", "credits": 3}
    ).json

    payload = {"student_id": student["id"], "course_id": course["id"]}
    first = client.post("/enrollments", json=payload)
    second = client.post("/enrollments", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_semester_credit_limit():
    client = setup_client()
    student = client.post(
        "/students",
        json={"name": "Neha", "email": "neha@example.com"}
    ).json

    for name, credits in [
        ("Course A", 6), ("Course B", 6), ("Course C", 6)
    ]:
        course = client.post(
            "/courses", json={"name": name, "credits": credits}
        ).json
        response = client.post(
            "/enrollments",
            json={"student_id": student["id"], "course_id": course["id"]}
        )
        assert response.status_code == 201

    extra = client.post(
        "/courses", json={"name": "Course D", "credits": 1}
    ).json
    response = client.post(
        "/enrollments",
        json={"student_id": student["id"], "course_id": extra["id"]}
    )
    assert response.status_code == 400
