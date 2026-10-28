from flask import Flask, jsonify, request

app = Flask(__name__)

# Demo-only in-memory data. Replace with a persistent database and authentication.
students = [
    {"id": 1, "name": "Sample Student", "course": "Computer Science"}
]
marks = []


@app.get("/api/health")
def health():
    return jsonify(status="UP", service="student-record-api")


@app.get("/api/students")
def get_students():
    return jsonify(students)


@app.post("/api/students")
def create_student():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    course = payload.get("course")
    if not isinstance(name, str) or not name.strip():
        return jsonify(error="name is required"), 400
    if not isinstance(course, str) or not course.strip():
        return jsonify(error="course is required"), 400
    student = {
        "id": max((item["id"] for item in students), default=0) + 1,
        "name": name.strip(),
        "course": course.strip(),
    }
    students.append(student)
    return jsonify(student), 201


@app.get("/api/marks")
def get_marks():
    return jsonify(marks)


@app.post("/api/marks")
def create_mark():
    payload = request.get_json(silent=True) or {}
    student_id = payload.get("student_id")
    subject = payload.get("subject")
    score = payload.get("score")
    if not isinstance(student_id, int) or not isinstance(subject, str):
        return jsonify(error="student_id (integer) and subject (string) are required"), 400
    if not isinstance(score, (int, float)) or not 0 <= score <= 100:
        return jsonify(error="score must be a number between 0 and 100"), 400
    record = {
        "id": len(marks) + 1,
        "student_id": student_id,
        "subject": subject.strip(),
        "score": score,
    }
    marks.append(record)
    return jsonify(record), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
