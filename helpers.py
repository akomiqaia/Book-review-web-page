import requests
from functools import wraps
from flask import session, redirect

# using goodreads API to get review cuonts and avarage raiting of the books
# fetched data will be displayed at books own page
def get_review_counts(isbn):
    api_key = "GACy0ylLEfy4uReswJrGOw"  
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"isbns": isbn, "key": api_key}).json()
    return res["books"][0]["reviews_count"]
def get_averadge_rating(isbn):
    api_key = "GACy0ylLEfy4uReswJrGOw"  
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"isbns": isbn, "key": api_key}).json()
    return res["books"][0]["average_rating"] 


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function