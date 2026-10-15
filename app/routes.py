from flask import Blueprint, jsonify, request

main = Blueprint("main", __name__)

students = []
courses = []
enrollments = []


@main.route("/")
def home():
    return jsonify({
        "message": "Student Academic Management Platform is running",
        "status": "success"
    })


@main.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@main.route("/students", methods=["GET", "POST"])
def manage_students():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        if not data.get("name") or not data.get("email"):
            return jsonify({"error": "name and email are required"}), 400

        student = {
            "id": len(students) + 1,
            "name": data["name"],
            "email": data["email"]
        }
        students.append(student)
        return jsonify(student), 201

    return jsonify(students)


@main.route("/courses", methods=["GET", "POST"])
def manage_courses():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        if not data.get("name") or not isinstance(data.get("credits"), int):
            return jsonify({
                "error": "name and integer credits are required"
            }), 400
        if data["credits"] < 1 or data["credits"] > 18:
            return jsonify({"error": "credits must be between 1 and 18"}), 400

        course = {
            "id": len(courses) + 1,
            "name": data["name"],
            "credits": data["credits"]
        }
        courses.append(course)
        return jsonify(course), 201

    return jsonify(courses)


@main.route("/enrollments", methods=["GET", "POST"])
def manage_enrollments():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        student_id = data.get("student_id")
        course_id = data.get("course_id")

        student = next((s for s in students if s["id"] == student_id), None)
        course = next((c for c in courses if c["id"] == course_id), None)

        if not student or not course:
            return jsonify({
                "error": "valid student_id and course_id required"
            }), 404

        if any(e["student_id"] == student_id and e["course_id"] == course_id
               for e in enrollments):
            return jsonify({
                "error": "student is already enrolled in this course"
            }), 409

        total_credits = sum(
            c["credits"] for e in enrollments
            if e["student_id"] == student_id
            for c in courses if c["id"] == e["course_id"]
        )
        if total_credits + course["credits"] > 18:
            return jsonify({"error": "semester credit limit is 18"}), 400

        enrollment = {
            "student_id": student_id,
            "course_id": course_id
        }
        enrollments.append(enrollment)
        return jsonify(enrollment), 201

    return jsonify(enrollments)
