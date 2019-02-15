import os
import json

from passlib.hash import pbkdf2_sha256
from helpers import get_review_counts, login_required, get_averadge_rating
from flask import Flask, session, request,render_template,redirect, url_for, jsonify
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
@login_required
def index():
    # when user logs in he has to see saerch tab where he can type
    # there will be random books displayed as well
    
    return render_template("index.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", errMessage="please provide username")
        if not request.form.get("password"):
            return render_template("error.html", errMessage="please provde password")
        if request.form.get("password") != request.form.get("password_confirmation"):
            return render_template("error.html", errMessage="password doesn't match")
        #  create hash for passwords and store it in database
        hashedPassword = pbkdf2_sha256.hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    { "username": request.form.get("username"), "password": hashedPassword})
        db.commit()
        return redirect("/")
    else:
        return render_template("register.html") 


@app.route("/login", methods=["GET", "POST"])
def login():
    # forget any user_id
    session.clear()
    if request.method == 'POST':
        user_name = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT username FROM users WHERE username = :user_name",
                        {"user_name": user_name}).fetchone()
        
        if not user:
            return render_template("error.html", errMessage="User does not exist")
        hashedPassword = pbkdf2_sha256.hash(password)

        if not pbkdf2_sha256.verify(password, hashedPassword):
            return render_template("error.html", errMessage="Passowrd is incorect")
        session["user"] = user
        return redirect('/')
    else:
        return render_template("login.html")

@app.route("/search", methods=['POST'])
@login_required
def search():
    # maybe imprve the highlighting of search. in the result page to dispaly table highlited where it was match.
    searchword = request.form.get("search")
    searchword = "%" + searchword + "%"
    books = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn ILIKE :searchword OR title ILIKE :searchword OR author ILIKE :searchword",
                            {"searchword": searchword}).fetchall()
    if not books:
        return render_template("error.html", errMessage="There is nothing in data-base with this keywords")  
    return render_template("search.html", bookList=books)

@app.route("/book/<isbn>", methods=["GET", "POST"])
@login_required
def bookInfo(isbn):
    if request.method == "POST":
        # user = db.execute("SELECT username FROM users WHERE username= :user",
        #                     {"user": session['user']})
        user_review = db.execute("SELECT * FROM reviews WHERE author = :username AND book_isbn = :isbn",
                            {"username": session["user"][0], "isbn": isbn} )
        userreview = user_review.first()
        if not userreview:
            review = request.form.get("review")
            rating = request.form.get("rating")
            db.execute("INSERT INTO reviews (review, book_isbn, rating, author) VALUES (:review, :book_isbn, :rating, :author)",
                        {"review": review, 'book_isbn': isbn, "rating": rating, "author": session["user"][0]})
            db.commit()
        else:
            return render_template("error.html", errMessage="you already submited review for this book")
        return redirect(url_for("bookInfo", isbn=isbn))
    else:
        book = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn",
                        {"isbn": isbn}).fetchone()
        reviews = db.execute("SELECT review FROM reviews WHERE book_isbn = :isbn",
                                {"isbn": isbn}).fetchall()
        averadgeRating = get_averadge_rating(book.isbn)
        reviewCount = get_review_counts(book.isbn)
        if not book:
            return render_template("error.html", errMessage="No such book")
        
        return render_template("bookInfo.html", book=book, reviews=reviews, averadgeRating=averadgeRating, reviewCount=reviewCount)
@app.route("/api/<isbn>")
def api(isbn):
    """ Return details about a single book."""

    # make sure book exists
    book = db.execute("SELECT title, author, year, isbn FROM books WHERE isbn= :isbn",
                    {"isbn": isbn}).fetchone()
    if not book:
        return jsonify({"error": "Invalid isbn"}), 422
    # get all the info needed for exporting
    reviewCount = get_review_counts(isbn)
    averageRating = get_averadge_rating(isbn)
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.year,
        "review_count": reviewCount,
        "average_score": averageRating
    })



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

