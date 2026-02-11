import os
import re
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# ---------------- COURSES DATABASE ----------------
COURSES = {
    "Diploma in IT": {
        "min_grade": "C",
        "faculty": "School of Computing and Informatics",
        "department": "Department of Information Technology"
    },
    "Computer Science": {
        "min_grade": "B+",
        "faculty": "School of Computing and Informatics",
        "department": "Department of Computer Science"
    },
    "Business Information Technology": {
        "min_grade": "B",
        "faculty": "School of Computing and Informatics",
        "department": "Department of Information Systems"
    },
    "Bachelor of Commerce": {
        "min_grade": "C+",
        "faculty": "Strathmore Business School",
        "department": "Department of Commerce"
    },
    "Law": {
        "min_grade": "B+",
        "faculty": "Strathmore Law School",
        "department": "Department of Law"
    },
    "Actuarial Science": {
        "min_grade": "A-",
        "faculty": "School of Finance and Applied Economics",
        "department": "Department of Actuarial Science"
    },
    "Statistics": {
        "min_grade": "B+",
        "faculty": "School of Finance and Applied Economics",
        "department": "Department of Statistics"
    }
}

# ---------------- GRADE ORDER ----------------
GRADE_ORDER = ["A", "A-", "B+", "B", "B-",
               "C+", "C", "C-", "D+", "D", "D-", "E"]

# ---------------- KEYWORDS ----------------
GREETINGS = ["hi", "hello", "hey", "start"]
THANKS = ["thanks", "thank you", "asante"]
POSTGRAD = ["degree", "bsc", "ba", "bcom", "undergraduate", "graduate"]

# ---------------- HELPERS ----------------


def normalize_grade(text):
    match = re.search(r"\b(a-|a|b\+|b-|b|c\+|c-|c|d\+|d-|d|e)\b", text.lower())
    return match.group(1).upper() if match else None


def eligible_courses(user_grade):
    user_index = GRADE_ORDER.index(user_grade)
    results = []
    for course, info in COURSES.items():
        if user_index <= GRADE_ORDER.index(info["min_grade"]):
            results.append(course)
    return results

# ---------------- ROUTES ----------------


@app.route("/")
def home():
    return "Welcome! Go to http://127.0.0.1:5000/chatbot to chat with Strathmore AI Assistant 🎓"


@app.route("/chatbot")
def chatbot():
    return send_from_directory(os.getcwd(), "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()

    # Greetings
    if user_message in GREETINGS:
        return jsonify({
            "reply": (
                "Hello! 👋 Welcome to Strathmore AI Assistant 🎓\n\n"
                "• Type your KCSE grade (e.g. A, B, C+)\n"
                "• Type Dip / Diploma in IT\n"
                "• Type a course name for more info\n"
                "• Type 1 to view all courses"
            )
        })

    # Thanks
    if any(word in user_message for word in THANKS):
        return jsonify({"reply": "You’re most welcome 😊 Happy to help!"})

    # View all courses
    if user_message == "1":
        reply = "📚 Available Courses:\n\n"
        for c, i in COURSES.items():
            reply += (
                f"• {c}\n"
                f"  Faculty: {i['faculty']}\n"
                f"  Department: {i['department']}\n"
                f"  Minimum Grade: {i['min_grade']}\n\n"
            )
        return jsonify({"reply": reply})

    # Postgraduate
    if any(word in user_message for word in POSTGRAD):
        return jsonify({
            "reply": (
                "🎓 Based on a completed degree, you may qualify for:\n\n"
                "• Master of Business Administration (MBA)\n"
                "• Master of Science in IT (MSc IT)\n\n"
                "Type a programme name to get more details."
            )
        })

    # Diploma recognition
    if "dip" in user_message:
        info = COURSES["Diploma in IT"]
        return jsonify({
            "reply": (
                "Course: Diploma in IT\n"
                f"Faculty: {info['faculty']}\n"
                f"Department: {info['department']}\n"
                f"Minimum Grade Required: {info['min_grade']}"
            )
        })

    # Course info
    for course in COURSES:
        if course.lower() in user_message:
            info = COURSES[course]
            return jsonify({
                "reply": (
                    f"Course: {course}\n"
                    f"Faculty: {info['faculty']}\n"
                    f"Department: {info['department']}\n"
                    f"Minimum Grade Required: {info['min_grade']}"
                )
            })

    # Grade handling (FIXED A / B issue ✅)
    grade = normalize_grade(user_message)
    if grade:
        courses = eligible_courses(grade)
        if courses:
            reply = "✅ Based on your grade, you qualify for:\n\n"
            for c in courses:
                reply += f"• {c}\n"
            reply += "\nType a course name to see more details."
            return jsonify({"reply": reply})

    # Fallback
    return jsonify({
        "reply": (
            "Sorry 😅, we couldn’t understand that.\n"
            "Please type your qualification (A, B, C+, Dip in IT),\n"
            "or type a course name to get more info."
        )
    })


@app.route("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


