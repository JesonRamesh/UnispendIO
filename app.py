import os
import csv
import logging
import datetime

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

WEEK_COUNTER = 1
TOTAL_DAYS = 0

COUNTRIES = []
with open("countries.csv", newline='') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        COUNTRIES.append(row)

db = SQL("sqlite:///userData.db")

EXPENSES = ["Education", "Groceries", "Entertainment", "Food", "Transportation", "Clothing", "Utilities", "Others"]

WEEK_NUMBERS = []
 #from cs50's finance project
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    global WEEK_COUNTER
    global DATE
    global TOTAL_DAYS
    global WEEK_NUMBERS

    user_id = session["user_id"]

    weekly_budget = db.execute("SELECT weekly_budget FROM users WHERE id=?", user_id)[0]["weekly_budget"]

    registered_date = db.execute("SELECT registered_date FROM users WHERE id=?", user_id)[0]["registered_date"]

    date = datetime.datetime.strptime(registered_date, "%Y-%m-%d").date()

    current_date = datetime.date.today()

    time_delta = (current_date - date)

    total_days = time_delta.days

    week_num = WEEK_COUNTER

    if (total_days//7) + 1 > week_num:
        remaining = weekly_budget
        WEEK_NUMBERS.append(week_num)
        WEEK_COUNTER = (total_days//7) + 1

    TOTAL_DAYS = total_days

    expenses = db.execute("SELECT type, amount, time, week FROM expenses WHERE user_id=? AND week=?", user_id, WEEK_COUNTER)

    total = 0
    for expense in expenses:
        total += expense["amount"]

    remaining = weekly_budget
    remaining -= total

    code = db.execute("SELECT currency_type FROM users WHERE id=?", user_id)[0]["currency_type"]


    return render_template("index.html", expenses=expenses, total=total, code=code, remaining=remaining, total_days = total_days)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("Must enter username!", 403)
        elif not password:
            return apology("Must enter password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Username and/or Password is invalid", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    global WEEK_COUNTER
    if request.method == "POST":
        expense = request.form.get("expense")
        amount = request.form.get("amount")
        week = WEEK_COUNTER

        if not expense:
            return apology("Please enter an expense!")
        elif not amount:
            return apology("Please enter an amount")

        try:
            amount = int(amount)
        except:
            return apology("Amount must be an integer!")

        if amount <= 0:
            return apology("Please enter a valid amount!")

        user_id = session["user_id"]

        time = datetime.datetime.now()
        time = time.ctime()

        db.execute("INSERT INTO expenses (user_id, type, amount, time, week) VALUES (?,?,?,?,?)",user_id, expense, amount, time, week)

        return redirect("/")

    else:
        return render_template("add.html", expenses=EXPENSES)

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():

    global WEEK_COUNTER

    user_id = session["user_id"]

    expenses = db.execute("SELECT id, type, amount, time FROM expenses WHERE user_id=? AND week=?", user_id, WEEK_COUNTER)
    code = db.execute("SELECT currency_type FROM users WHERE id=?", user_id)[0]["currency_type"]

    total = 0

    for expense in expenses:
        total += expense["amount"]

    if request.method == "POST":
        id = request.form.get("id")

        try:
            id = int(id)
            db.execute("DELETE FROM expenses WHERE id=? AND user_id=?", id, user_id)
        except:
            return apology("Cannot remove expense because it doesn't exist.")

        return redirect("/")

    else:
        return render_template("remove.html", expenses=expenses, total=total, code=code)


@app.route("/change", methods=["GET", "POST"])
def change():
    user_id = session["user_id"]
    current_weekly_budget = db.execute("SELECT weekly_budget FROM users WHERE id = ?", user_id)[0]["weekly_budget"]
    code = db.execute("SELECT currency_type FROM users WHERE id=?", user_id)[0]["currency_type"]

    if request.method == "POST":
        newBudget = request.form.get("newBudget")

        if not newBudget:
            return apology("Please enter a value for the new budget!")

        try:
            newBudget = int(newBudget)
        except:
            return apology("Please enter an integer value for the budget!")

        if newBudget <= 0:
            return apology("Please enter a positive integer value for the budget!")

        db.execute("UPDATE users SET weekly_budget = ? WHERE id = ?", newBudget, user_id)

        return redirect("/")

    else:
        return render_template("/change.html", current_weekly_budget=current_weekly_budget, code=code)


@app.route("/register", methods=["GET","POST"])
def register():
    if (request.method == "POST"):
        username = request.form.get("username")
        country = request.form.get("country")
        weekly_budget = request.form.get("weekly_budget")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please enter a username!")
        elif not password:
            return apology("Please enter a password!")
        elif not confirmation:
            return apology("Please confirm your password!")

        all_users = db.execute("SELECT username FROM users")[0]["username"]

        for user in all_users:
            if username == user:
                return apology("Username already taken")

        if not country:
            return apology("Please select a country!")

        if not weekly_budget:
            return apology("Please enter a weekly budget goal!")
        elif not weekly_budget.isdigit() or int(weekly_budget) <= 0:
            return apology("Please enter a positive integer value for the weekly budget!")
        else:
            weekly_budget = int(weekly_budget)

        if password != confirmation:
            return apology("Passwords do not match!")

        hashed_password = generate_password_hash(password)

        code = ""

        for coun in COUNTRIES:
            if coun["entity"].strip().lower() == country.strip().lower():
                code = coun["alphabetic_code"]

        if code == "":
            return apology("Please select a different country!")

        date = datetime.date.today()

        try:
            db.execute("INSERT INTO users (username, hash, country, currency_type, weekly_budget, registered_date) VALUES (?,?,?,?,?,?)", username, hashed_password, country, code, weekly_budget, date)
            return redirect("/")
        except:
            return apology("User already registered")
    else:
        return render_template("register.html", countries=COUNTRIES)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/weeklysummary")
def weekly_summary():
    return render_template("weeklysummary.html", week_numbers=WEEK_NUMBERS, len=len)

@app.route("/weeklysummary/<week_number>")
def summary(week_number):
    user_id = session["user_id"]
    expenses = db.execute("SELECT type, amount FROM expenses WHERE user_id=? AND week=? GROUP BY type", user_id, week_number)
    weekly_budget = db.execute("SELECT weekly_budget FROM users WHERE id = ?", user_id)[0]["weekly_budget"]

    total = 0
    for expense in expenses:
        total += expense["amount"]

    remaining = weekly_budget - total

    code = db.execute("SELECT currency_type FROM users WHERE id=?", user_id)[0]["currency_type"]

    return render_template("summary.html", week_number=week_number, expenses=expenses, total=total, code=code, remaining=remaining)

if __name__ == "__main__":
    app.run(debug=True)


