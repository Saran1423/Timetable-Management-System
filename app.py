from flask import Flask, render_template, request, redirect, session
import json, os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATA ----------
def load_timetable():
    if not os.path.exists("timetable.json"):
        with open("timetable.json", "w") as f:
            json.dump({"timetable": []}, f)

    with open("timetable.json") as f:
        return json.load(f)

def save_timetable(data):
    with open("timetable.json", "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({"users": []}, f)

    with open("users.json") as f:
        return json.load(f)

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- ROUTES ----------

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    data = load_timetable()
    return render_template("index.html",
                           timetable=data["timetable"],
                           user=session["user"],
                           role=session.get("role"))

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        users = load_users()
        for u in users["users"]:
            if u["username"] == request.form["username"] and u["password"] == request.form["password"]:
                session["user"] = u["username"]
                session["role"] = u.get("role","student")
                return redirect("/")
        return render_template("login.html", error="Invalid login")

    return render_template("login.html")

# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        users = load_users()

        # prevent duplicate
        for u in users["users"]:
            if u["username"] == request.form["username"]:
                return render_template("register.html", error="User already exists")

        users["users"].append({
            "username": request.form["username"],
            "password": request.form["password"],
            "role": "student"
        })

        save_users(users)
        return redirect("/login")

    return render_template("register.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ADD CLASS (ADMIN ONLY)
@app.route("/add", methods=["POST"])
def add():
    if session.get("role") != "admin":
        return "Access Denied"

    data = load_timetable()

    new_class = {
        "id": len(data["timetable"]) + 1,
        "subject": request.form["subject"],
        "faculty": request.form["faculty"],
        "day": request.form["day"],
        "time": request.form["time"],
        "room": request.form["room"]
    }

    data["timetable"].append(new_class)
    save_timetable(data)

    return redirect("/")

# DELETE CLASS
@app.route("/delete/<int:id>")
def delete(id):
    if session.get("role") != "admin":
        return "Access Denied"

    data = load_timetable()
    data["timetable"] = [c for c in data["timetable"] if c["id"] != id]
    save_timetable(data)

    return redirect("/")

# SETTINGS
@app.route("/settings")
def settings():
    if "user" not in session:
        return redirect("/login")

    return render_template("settings.html", user=session["user"])

# RUN
if __name__ == "__main__":
    app.run(debug=True)