import os
import json
from helpers import get_review_counts, error_message
from flask import Flask, session, request,render_template,redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up databaseimport requests

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return get_review_counts("0743454553")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return error_message("please provide username")
        if not request.form.get("password"):
            return error_message("please provde password")
        if request.form.get("password") != request.form.get("password_confirmation"):
            return error_message("password doesn't match")
        
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    { "username": request.form.get("username"), "password": request.form.get("password")})
        db.commit()
        return render_template("index.html")
    else:
        return render_template("register.html")
    return render_template("register.html") 

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return render_template("login.html")

