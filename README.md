#1 Project 1 - Book Review Web page


**The project is done as an assignment for CS50 course in Web Programming.**

_Project uses Bootstrap to decorate HTML. On the server side web-page uses python with FLask framework and ORM(ObjectRelationalMapper)SQLAlchemy library_

**To run project:**
1. Download or clone git repository https://github.com/akomiqaia/Book-review-web-page.git
2. From your terminal in the repository folder ```export FLASK_APP=application.py```
3. Then ```export FLASK_ENV=development```
4. Then ```export DATABASE_URL="postgres://ftkelgeppoihqs:e426f6a7ee01c64a3473b96af7a4f5ae2d40ff532224f85966cc37b6ba52157e@ec2-54-246-117-62.eu-west-1.compute.amazonaws.com:5432/d497eaccus6eki"``` to set environmental variable equal to the link of my database of books.
5. Run ```flask run```


__Objectives achieved while working on the project:__


- **Basic User Functionality**: Users can login, register and log out.
- **Import**: The book database was imported by python file called import.py, that puts csv file content into database, that is hosted on Heroku 
- **Search**: Once a user has logged in, they are taken to a page where they can search for a book. Users are able search with the ISBN number of a book, the title of a book, or the author of a book. After performing the search, the website displays a list of possible matching results, or error message if there were no matches. If the user typed in only part of a title, ISBN, or author name, the search page can find matches for those as well!
- **Book Page**: When users click on a book from the results of the search page, they are taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
- **Review Submission**: On the book page, users can submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users can not submit multiple reviews for the same book. 
- **Goodreads Review Data**: On the book page, you should be able to see (if available) the average rating and number of ratings the work has received from Goodreads.
- **API Access**: Users  can make a GET request to the website’s /api/<isbn> route, where <isbn> is an ISBN number of the book, the website returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON follows the format:
```JSON
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
```
If the requested ISBN number isn’t in the database, the website returns a 404 error.

