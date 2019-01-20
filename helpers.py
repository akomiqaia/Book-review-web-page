import requests


def get_review_counts(isbn):
  api_key = "GACy0ylLEfy4uReswJrGOw"  
  res = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"isbns": isbn, "key": api_key}).json()
  return res["books"][0]["average_rating"]

def error_message(err):
  return err