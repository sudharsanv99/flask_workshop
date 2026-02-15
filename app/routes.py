from app import app
from flask import render_template, request, current_app
from datetime import datetime
import os

current_login = None

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route("/login" , methods = ["POST", "GET"])
def login():
    global current_login
    if request.method == "POST":
        current_login = request.form.get("username")
        return render_template("confirmation.html", current_login = current_login)
    return render_template("login.html")

@app.route("/ticket", methods = ["GET", "POST"])
def ticket():
    global current_login
    tickets = ['Unable to login', 'No browser access', 'Unable to access core']
    if request.method == "POST":
        ticket = request.form.get("problem_to_be_resolved")
        current_login = request.form.get("username")
        today_date = datetime.today().date()
        file_path = os.path.join(
            current_app.root_path, "static", "problems.txt"
        )
        with open(file_path, "a") as file:
            file.write(f"{current_login} | {ticket} | {today_date} \n")
        return render_template("ticket_confirm.html", current_login = current_login, date = today_date)
    return render_template("ticket.html",ticket_list = tickets)




@app.route('/labs', methods = ["GET", "POST"])
def labs():
    global current_login
    times = ['09:00', '11:00', '13:00', '15:00']
    if request.method == "POST":
        current_login = request.form.get("username")
        time_slot_selected = request.form.get("lab_timings")
        return render_template("lab_confirm.html",
                               current_login = current_login, time_slot_selected = time_slot_selected)
    return render_template("labs.html", times = times)

@app.route('/listing',methods = ["GET", "POST"])
def listing():
    global current_login
    if request.method == "POST":
        completed = request.form.getlist("completed")
        return render_template("resolved.html",completed = completed)
    file_path = os.path.join(current_app.root_path, "static", "problems.txt")
    ticket_to_be_completed = []
    with open(file_path, "r") as file:
        for line in file:
            ticket_to_be_completed.append(line)
    if current_login == "admin":
        return render_template("listing.html", ticket_to_be_completed = ticket_to_be_completed)
    else:
        return render_template("base.html")


