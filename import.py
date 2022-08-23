import csv
import os

from flask import Flask, session, render_template, request
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

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	db.execute("CREATE TABLE books(isbn VARCHAR primary key , title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL)")
	db.execute("CREATE TABLE users(id SERIAL primary key unique, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
	db.execute("CREATE TABLE reviews(id SERIAL primary key , users_id INTEGER NOT NULL REFERENCES users,\
		books_isbn VARCHAR NOT NULL REFERENCES books, rating VARCHAR NOT NULL, review VARCHAR NULL)")

	f=open("books.csv")
	reader= csv.reader(f)
	for isbn,title,author,year in reader:
		if isbn != "isbn":
			db.execute("INSERT INTO books (isbn, title, author, year) VALUES ( :isbn, :title, :author, :year)", 
				{"isbn":isbn, "title":title, "author":author, "year":year})
	db.commit()

if __name__ == "__main__":
	main()

