create table users(id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR);

create table books(isbn VARCHAR PRIMARY KEY, title VARCHAR, author VARCHAR, year INTEGER);

create table reviews(id SERIAL PRIMARY KEY, reviews VARCHAR NOT NULL, user_id INTEGER REFERENCES users, book_isbn VARCHAR REFERENCES books, stars INTEGER);
