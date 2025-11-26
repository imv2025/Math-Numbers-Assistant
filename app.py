import os
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///myproject.db")


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        # Escape special characters:
        # https://github.com/jacebrowning/memegen#special-characters
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    # Decorate routes to require login.
    # https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear previous session
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("confirm your password", 400)
        # Ensure password was twice equally submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # username exists?
        if len(rows) != 0:
            return apology("username already exists", 400)

        # hash the password before than inserting to db
        password = generate_password_hash(request.form.get("password"))
        # add new valid user values to DB
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   request.form.get("username"), password)
        # search for the registered user
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))
        # create a new session for the user
        session["user_id"] = rows[0]["id"]
        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/")
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    return render_template("index.html")


@app.route("/calculator")
@login_required
def calculator():
    return render_template("calculator.html")


@app.route("/abundantnumbers")
@login_required
def abundantnumbers():
    return render_template("/abundantnumbers.html")


@app.route("/evennumbers")
@login_required
def evennumbers():
    return render_template("evennumbers.html")


@app.route("/primenumbers")
@login_required
def primenumbers():
    return render_template("primenumbers.html")


@app.route("/narcissticnumbers")
@login_required
def narcissticnumbers():
    return render_template("/narcissticnumbers.html")


@app.route("/pronicnumbers")
@login_required
def pronicnumbers():
    return render_template("/pronicnumbers.html")


@app.route("/me")
@login_required
def me():
    return render_template("me.html")
