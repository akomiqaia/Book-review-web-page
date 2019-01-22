create table users(id SERIAL, username VARCHAR PRIMARY KEY, password VARCHAR);

create table books(isbn VARCHAR PRIMARY KEY, title VARCHAR, author VARCHAR, year INTEGER);

create table reviews(id SERIAL PRIMARY KEY, review VARCHAR NOT NULL, book_isbn VARCHAR REFERENCES books, rating INTEGER, author VARCHAR REFERENCES users);
