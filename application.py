import os
import requests

from flask import Flask, session, request
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

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"GACy0ylLEfy4uReswJrGOw": "KEY", "isbns": "9781632168146"})
if res.status_code != 200:
    raise Exception("ERROR: API reqsuet unsuccesful")
print(res.json())

@app.route("/")
def index():
    return "API"

