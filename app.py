import re

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
# Above almost copied from "https://cs50.harvard.edu/x/psets/9/finance/"


@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")

        row = db.execute("SELECT * FROM user WHERE username = ?", username)
        if len(row) != 1:
            return apology("user doesn't exist")
        hash = row[0]["hash"]
        if not check_password_hash(hash, password):
            return apology("password incorrect")

        session["user_id"] = row[0]["id"]

        return redirect("/")
    return render_template("login.html")


# This route is completed with help of AI technology.
@app.route("/")
@login_required
def index():
    courses = db.execute("SELECT * FROM course")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grids = [[None for _ in range(7)] for _ in range(14)]

    for course in courses:
        times = course["time"]
        time = times.split(',')
        lens = len(time)
        str_days = [None] * lens
        segs = [None] * lens
        start = [None] * lens
        end = [None] * lens
        for i in range(0, lens):
            str_days[i], segs[i] = time[i].split()

        for j in range(0, lens):
            try:
                idx_day = days.index(str_days[j])
            except ValueError:
                return apology("must provide valid time")

            idx_day = days.index(str_days[j])
            if "-" in segs[j]:
                start[j], end[j] = map(int, segs[j].split("-"))
            else:
                start[j] = end[j] = int(segs[j])
            for i in range(start[j], end[j] + 1):
                grids[i - 1][idx_day] = {
                    "name": course["name"],
                    "teacher": course["teacher"],
                    "site": course["site"]
                }

    return render_template("index.html", grids=grids)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")

        data = db.execute("SELECT * FROM user WHERE username = ?", username)
        if len(data) != 0:
            return apology("sorry, username has been occupied")

        db.execute("INSERT INTO user (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        return redirect("/login")
    return render_template("register.html")


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    session.clear()

    return redirect("/login")


@app.route("/add", methods=["POST", "GET"])
@login_required
def route():
    if request.method == "POST":
        coursename = request.form.get("coursename")
        courseteacher = request.form.get("courseteacher")
        coursesite = request.form.get("coursesite")
        coursetime = request.form.get("coursetime")

        if not coursename or not courseteacher or not coursesite or not coursetime:
            return apology("must provide complete information")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time = coursetime.split(',')
        lens = len(time)
        segs = [None] * lens
        str_days = [None] * lens
        for i in range(0, lens):
            str_days[i], segs[i] = time[i].split()
        for j in range(0, lens):
            try:
                idx_day = days.index(str_days[j])
            except ValueError:
                return apology("must provide valid time")

        db.execute("INSERT INTO course (name, teacher, site, time) VALUES(?, ?, ?, ?)", coursename, courseteacher, coursesite, coursetime)
        return render_template("add.html")
    return render_template("add.html")


@app.route("/update", methods=["POST", "GET"])
@login_required
def update():
    if request.method == "POST":
        originname = request.form.get("originname")
        originteacher = request.form.get("originteacher")
        originsite = request.form.get("originsite")
        origintime = request.form.get("origintime")
        newname = request.form.get("newname")
        newteacher = request.form.get("newteacher")
        newsite = request.form.get("newsite")
        newtime = request.form.get("newtime")

        if not originname or not originteacher or not originsite or not origintime or not newname or not newteacher or not newsite or not newtime:
            return apology("must provide complete information")

        data = db.execute("SELECT * FROM course WHERE name = ? AND teacher = ? AND site = ? AND time = ?", originname, originteacher, originsite, origintime)
        if len(data) == 0:
            return apology("sorry, course(s) not found")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time = newtime.split(',')
        lens = len(time)
        segs = [None] * lens
        str_days = [None] * lens
        for i in range(0, lens):
            str_days[i], segs[i] = time[i].split()
        for j in range(0, lens):
            try:
                idx_day = days.index(str_days[j])
            except ValueError:
                return apology("must provide valid time")

        db.execute("UPDATE course SET name = ?, teacher = ?, site = ?, time = ? WHERE name = ? AND teacher = ? AND site = ? AND time = ?", newname, newteacher, newsite, newtime, originname, originteacher, originsite, origintime)
        return render_template("update.html")
    return render_template("update.html")


@app.route("/changepw", methods=["POST", "GET"])
@login_required
def changepw():
    if request.method == "POST":
        old = request.form.get("oldpassword")
        new = request.form.get("newpassword")

        if not old or not new:
            return apology("must provide these two passwords")

        hash = db.execute("SELECT * FROM user WHERE id = ?", session["user_id"])[0]["hash"]
        if not check_password_hash(hash, old):
            return apology("original password incorrect")

        db.execute("UPDATE user SET hash = ? WHERE id = ?", generate_password_hash(new), session["user_id"])
        session.clear()
        return render_template("login.html")

    return render_template("changepw.html")
