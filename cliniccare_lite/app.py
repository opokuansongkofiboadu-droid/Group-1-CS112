import os
import json
import re
import bcrypt

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")
TASKS_FILE = os.path.join(BASE_DIR, "data", "tasks.json")

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

    return render_template(
        "patient_dashboard.html",
        name=session["full_name"]
    )


@app.route("/clinician-dashboard")
def clinician_dashboard():
    if "user_id" not in session or session["role"] != "clinician":
        return redirect(url_for("login"))

    return render_template(
        "clinician_dashboard.html",
        name=session["full_name"]
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


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)