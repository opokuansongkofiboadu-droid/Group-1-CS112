import os
import json
import re
import bcrypt
import csv

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory
)
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")
TASKS_FILE = os.path.join(BASE_DIR, "data", "tasks.json")
SUBMISSIONS_FILE = os.path.join(BASE_DIR, "data", "submissions.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MESSAGES_FILE = os.path.join(BASE_DIR, "data", "messages.json")
ANNOUNCEMENTS_FILE = os.path.join(
    BASE_DIR, "data", "announcements.json")
APPOINTMENTS_FILE = os.path.join(
    BASE_DIR, "data", "appointments.json"
)
MAX_FILE_SIZE = 5 * 1024 * 1024


def load_users():
    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def load_tasks():
    with open(TASKS_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def load_submissions():
    with open(SUBMISSIONS_FILE, "r") as file:
        return json.load(file)


def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, "w") as file:
        json.dump(submissions, file, indent=4)

def load_messages():
    with open(MESSAGES_FILE, "r") as file:
        return json.load(file)


def save_messages(messages):
    with open(MESSAGES_FILE, "w") as file:
        json.dump(messages, file, indent=4)

def load_announcements():
    with open(ANNOUNCEMENTS_FILE, "r") as file:
        return json.load(file)


def save_announcements(announcements):
    with open(ANNOUNCEMENTS_FILE, "w") as file:
        json.dump(announcements, file, indent=4)

def load_appointments():
    with open(APPOINTMENTS_FILE, "r") as file:
        return json.load(file)


def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, "w") as file:
        json.dump(appointments, file, indent=4)

def check_file_completeness(file_path, extension):

    if extension == "txt":
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            return "Incomplete: TXT file is empty."

        return "Complete"


    if extension == "csv":
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

        if len(rows) == 0:
            return "Incomplete: CSV file is empty."

        if len(rows[0]) == 0:
            return "Incomplete: CSV has no headings."

        if len(rows) < 2:
            return "Incomplete: CSV has no data rows."

        for row in rows:
            for cell in row:
                if cell.strip() == "":
                    return "Incomplete: CSV contains empty fields."

        return "Complete"


    if extension == "pdf":
        return "Accepted - PDF completeness not automatically checked."

    return "Unsupported file type."

def valid_user_id(user_id, role):
    if not user_id.isdigit() or len(user_id) != 8:
        return False

    if role == "clinician":
        return user_id.endswith("0000")

    if role == "patient":
        year = int(user_id[-4:])
        return 2022 <= year <= 2028

    return False


def valid_password(password):
    return (
        len(password) >= 8
        and any(char.isupper() for char in password)
        and any(char.islower() for char in password)
        and any(char.isdigit() for char in password)
        and bool(re.search(r"[!@#$%^&*]", password))
    )


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        role = request.form["role"]
        user_id = request.form["user_id"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        if not valid_user_id(user_id, role):
            message = "Invalid user ID."

        elif not valid_password(password):
            message = "Password does not meet the requirements."

        else:
            users = load_users()

            for user in users:
                if user["user_id"] == user_id:
                    message = "User ID already registered."
                    return render_template("register.html", message=message)

            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            new_user = {
                "user_id": user_id,
                "full_name": full_name,
                "email": email,
                "password": hashed_password,
                "role": role
            }

            users.append(new_user)
            save_users(users)

            return redirect(url_for("login"))

    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        user_id = request.form["user_id"].strip()
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["user_id"] == user_id:

                correct_password = bcrypt.checkpw(
                    password.encode("utf-8"),
                    user["password"].encode("utf-8")
                )

                if correct_password:
                    session["user_id"] = user["user_id"]
                    session["full_name"] = user["full_name"]
                    session["role"] = user["role"]

                    if user["role"] == "patient":
                        return redirect(url_for("patient_dashboard"))

                    if user["role"] == "clinician":
                        return redirect(url_for("clinician_dashboard"))

                message = "Incorrect password."
                return render_template("login.html", message=message)

        message = "User ID not found."

    return render_template("login.html", message=message)


@app.route("/patient-dashboard")
def patient_dashboard():
    if "user_id" not in session or session["role"] != "patient":
        return redirect(url_for("login"))

    tasks = load_tasks()
    submissions = load_submissions()
    messages = load_messages()
    announcements = load_announcements()
    appointments = load_appointments()

    patient_appointments = []

    for appointment in appointments:
        if appointment["patient_id"] == session["user_id"]:
            patient_appointments.append(appointment)

    patient_tasks = []

    for task in tasks:
        if task["patient_id"] == session["user_id"]:

            task_info = task.copy()

            task_info["review_outcome"] = ""
            task_info["review_notes"] = ""

            for submission in submissions:
                if (
                    submission["task_id"] == task["task_id"]
                    and submission["patient_id"] == session["user_id"]
                ):
                    task_info["review_outcome"] = submission.get(
                        "review_outcome", ""
                    )
                    task_info["review_notes"] = submission.get(
                        "review_notes", ""
                    )

            patient_tasks.append(task_info)

    patient_messages = []

    for message in messages:
        if message["recipient_id"] == session["user_id"]:
            patient_messages.append(message)   

    users = load_users()
    engagement_points = 0

    for user in users:
        if user["user_id"] == session["user_id"]:
            engagement_points = user.get("engagement_points", 0)
            break    

    theme = session.get("theme", "colorful")

    return render_template(
        "patient_dashboard.html",
        name=session["full_name"],
        tasks=patient_tasks,
        messages=patient_messages,
        engagement_points=engagement_points,
        announcements=announcements,
        appointments=patient_appointments,
        theme=theme
    )

@app.route("/clinician-dashboard")
def clinician_dashboard():
    if "user_id" not in session or session["role"] != "clinician":
        return redirect(url_for("login"))

    tasks = load_tasks()
    submissions = load_submissions()
    messages = load_messages()

    clinician_tasks = []

    for task in tasks:
        if task["clinician_id"] == session["user_id"]:
            clinician_tasks.append(task)

    clinician_submissions = []

    for submission in submissions:
        for task in clinician_tasks:
            if task["task_id"] == submission["task_id"]:
                submission_info = submission.copy()
                submission_info["task_title"] = task["title"]
                clinician_submissions.append(submission_info)

    clinician_messages = []

    for message in messages:
        if message["recipient_id"] == session["user_id"]:
            clinician_messages.append(message)

    total_tasks = len(clinician_tasks)
    total_submissions = len(clinician_submissions)

    reviewed = 0
    pending_reviews = 0

    for submission in clinician_submissions:
        if submission["status"] == "Reviewed":
            reviewed += 1
        else:
            pending_reviews += 1

    if total_tasks > 0:
        completion_rate = round((reviewed / total_tasks) * 100, 1)
    else:
        completion_rate = 0

    return render_template(
        "clinician_dashboard.html",
        name=session["full_name"],
        submissions=clinician_submissions,
        messages=clinician_messages,
        total_tasks=total_tasks,
        total_submissions=total_submissions,
        reviewed=reviewed,
        pending_reviews=pending_reviews,
        completion_rate=completion_rate
    )

@app.route("/create-task", methods=["POST"])
def create_task():

    if "user_id" not in session or session["role"] != "clinician":
        return redirect(url_for("login"))

    patient_id = request.form["patient_id"].strip()
    title = request.form["title"].strip()
    description = request.form["description"].strip()
    due_date = request.form["due_date"]

    users = load_users()

    patient_exists = False

    for user in users:
        if user["user_id"] == patient_id and user["role"] == "patient":
            patient_exists = True
            break

    if not patient_exists:
        return render_template(
            "clinician_dashboard.html",
            name=session["full_name"],
            message="Patient ID not found."
        )

    tasks = load_tasks()

    new_task = {
        "task_id": len(tasks) + 1,
        "patient_id": patient_id,
        "clinician_id": session["user_id"],
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "Pending"
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return render_template(
        "clinician_dashboard.html",
        name=session["full_name"],
        message="Task assigned successfully!"
    )

@app.route("/submit-task/<int:task_id>", methods=["POST"])
def submit_task(task_id):

    if "user_id" not in session or session["role"] != "patient":
        return redirect(url_for("login"))

    tasks = load_tasks()

    task = None

    for item in tasks:
        if (
            item["task_id"] == task_id
            and item["patient_id"] == session["user_id"]
        ):
            task = item
            break

    if task is None:
        return "Task not found or unauthorized.", 403

    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return "Please select a file."

    extension = uploaded_file.filename.rsplit(".", 1)[-1].lower()

    if extension not in ["txt", "csv", "pdf"]:
        return "Only TXT, CSV and PDF files are allowed."

    file_data = uploaded_file.read()
    file_size = len(file_data)

    uploaded_file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return "File is too large. Maximum size is 5 MB."

    submissions = load_submissions()

    for submission in submissions:
        if (
            submission["task_id"] == task_id
            and submission["patient_id"] == session["user_id"]
        ):
            return "You have already submitted this task."

    patient_folder = os.path.join(
        UPLOAD_FOLDER,
        session["user_id"]
    )

    os.makedirs(patient_folder, exist_ok=True)

    new_filename = (
        f"{session['user_id']}_task{task_id}.{extension}"
    )

    file_path = os.path.join(patient_folder, new_filename)

    uploaded_file.save(file_path)
    completeness_result = check_file_completeness(
    file_path,
    extension
)

    new_submission = {
        "submission_id": len(submissions) + 1,
        "task_id": task_id,
        "patient_id": session["user_id"],
        "filename": new_filename,
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Submitted",
        "completeness_check": completeness_result,
        "review_outcome": "",
        "review_notes": ""
    }

    submissions.append(new_submission)
    save_submissions(submissions)

    messages = load_messages()

    notification = {
        "message_id": len(messages) + 1,
        "sender_id": session["user_id"],
        "recipient_id": task["clinician_id"],
        "content": f"New submission received for task: {task['title']}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False
}

    messages.append(notification)
    save_messages(messages)


    task["status"] = "Submitted"
    save_tasks(tasks)

    users = load_users()

    for user in users:
        if user["user_id"] == session["user_id"]:
            current_points = user.get("engagement_points", 0)
            user["engagement_points"] = current_points + 10
            break

    save_users(users)

    return redirect(url_for("patient_dashboard"))

    messages = load_messages()

    notification = {
     "message_id": len(messages) + 1,
        "sender_id": session["user_id"],
        "recipient_id": task["clinician_id"],
        "content": f"New submission received for task: {task['title']}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False
}

    messages.append(notification)
    save_messages(messages)

    

@app.route("/review-submission/<int:submission_id>", methods=["POST"])
def review_submission(submission_id):

    if "user_id" not in session or session["role"] != "clinician":
        return redirect(url_for("login"))

    review_outcome = request.form["review_outcome"]
    review_notes = request.form["review_notes"].strip()

    submissions = load_submissions()

    for submission in submissions:

        if submission["submission_id"] == submission_id:

            submission["status"] = "Reviewed"
            submission["review_outcome"] = review_outcome
            submission["review_notes"] = review_notes
            submission["reviewer_id"] = session["user_id"]
            submission["reviewed_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            submission["notification_status"] = "Sent"

            save_submissions(submissions)

            # Send automatic notification to patient
            messages = load_messages()

            notification = {
                "message_id": len(messages) + 1,
                "sender_id": session["user_id"],
                "recipient_id": submission["patient_id"],
                "content": f"Your submission has been reviewed: {review_outcome}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read": False
            }

            messages.append(notification)
            save_messages(messages)

            # Update task status
            tasks = load_tasks()

            for task in tasks:
                if task["task_id"] == submission["task_id"]:
                    task["status"] = "Reviewed"
                    break

            save_tasks(tasks)

            break

    return redirect(url_for("clinician_dashboard"))

@app.route("/send-message", methods=["POST"])
def send_message():

    if "user_id" not in session:
        return redirect(url_for("login"))

    recipient_id = request.form["recipient_id"].strip()
    content = request.form["content"].strip()

    users = load_users()

    recipient_exists = False

    for user in users:
        if user["user_id"] == recipient_id:
            recipient_exists = True
            break

    if not recipient_exists:
        return "Recipient not found."

    messages = load_messages()

    new_message = {
        "message_id": len(messages) + 1,
        "sender_id": session["user_id"],
        "recipient_id": recipient_id,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False
    }

    messages.append(new_message)
    save_messages(messages)

    if session["role"] == "patient":
        return redirect(url_for("patient_dashboard"))

    return redirect(url_for("clinician_dashboard"))

@app.route("/create-announcement", methods=["POST"])
def create_announcement():

    if "user_id" not in session or session["role"] != "clinician":
        return redirect(url_for("login"))

    title = request.form["title"].strip()
    content = request.form["content"].strip()
    priority = request.form["priority"]

    announcements = load_announcements()

    new_announcement = {
        "announcement_id": len(announcements) + 1,
        "title": title,
        "content": content,
        "priority": priority,
        "clinician_id": session["user_id"],
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    announcements.append(new_announcement)
    save_announcements(announcements)

    return redirect(url_for("clinician_dashboard"))

@app.route("/create-appointment", methods=["POST"])
def create_appointment():

    if "user_id" not in session or session["role"] != "clinician":
        return redirect(url_for("login"))

    patient_id = request.form["patient_id"].strip()
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]
    purpose = request.form["purpose"].strip()

    users = load_users()

    patient_exists = False

    for user in users:
        if user["user_id"] == patient_id and user["role"] == "patient":
            patient_exists = True
            break

    if not patient_exists:
        return "Patient ID not found."

    appointments = load_appointments()

    new_appointment = {
        "appointment_id": len(appointments) + 1,
        "patient_id": patient_id,
        "clinician_id": session["user_id"],
        "date": appointment_date,
        "time": appointment_time,
        "purpose": purpose,
        "status": "Scheduled"
    }

    appointments.append(new_appointment)
    save_appointments(appointments)

    return redirect(url_for("clinician_dashboard"))

@app.route("/change-theme", methods=["POST"])
def change_theme():

    if "user_id" not in session or session["role"] != "patient":
        return redirect(url_for("login"))

    theme = request.form["theme"]

    if theme in ["colorful", "dark"]:
        session["theme"] = theme

    return redirect(url_for("patient_dashboard"))

@app.route("/download-submission/<int:submission_id>")
def download_submission(submission_id):

    if "user_id" not in session or session["role"] != "clinician":
        return redirect(url_for("login"))

    submissions = load_submissions()
    tasks = load_tasks()

    for submission in submissions:

        if submission["submission_id"] == submission_id:

            # Check that this submission belongs to
            # a task created by the logged-in clinician.
            allowed = False

            for task in tasks:
                if (
                    task["task_id"] == submission["task_id"]
                    and task["clinician_id"] == session["user_id"]
                ):
                    allowed = True
                    break

            if not allowed:
                return "Unauthorized.", 403

            patient_folder = os.path.join(
                UPLOAD_FOLDER,
                submission["patient_id"]
            )

            return send_from_directory(
                patient_folder,
                submission["filename"],
                as_attachment=True
            )

    return "Submission not found.", 404

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)