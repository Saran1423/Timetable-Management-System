@app.route("/add", methods=["POST"])
def add():
    if session.get("role") != "admin":
        return "Access Denied"

    data = load_timetable()

    new_class = {
        "id": len(data["timetable"]) + 1,
        "subject": request.form.get("subject"),
        "faculty": request.form.get("faculty"),
        "day": request.form.get("day"),
        "time": request.form.get("time"),
        "room": request.form.get("room"),
        "department": request.form.get("department"),
        "section": request.form.get("section"),
        "type": request.form.get("type")
    }

    data["timetable"].append(new_class)
    save_timetable(data)

    return redirect("/")
