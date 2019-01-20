import requests


def get_review_Counts(isbn):
  api_key = "GACy0ylLEfy4uReswJrGOw"  
  res = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"isbns": isbn, "key": api_key}) 
  return res.json()
# res = requests.get( params={"key":"", "isbns": "9781632168146"})

# data = res.json()
