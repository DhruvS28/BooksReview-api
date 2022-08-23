import csv
import os
import re
import requests

from flask import Flask, session, render_template, request, session
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

# Set up database postgres://vcklheqsokdoia:78680f64d1685e0654b11f8362d1d616dbc3d0a92f362a3a6b42c3db32c4ff87@ec2-34-203-182-65.compute-1.amazonaws.com:5432/d629k487drgvc8
url = os.getenv("DATABASE_URL")
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

engine = create_engine(url)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["POST", "GET"])
def index1():

	db.execute("ROLLBACK")
	db.commit()

	try:
		db.execute("CREATE TABLE books(isbn VARCHAR primary key , title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL)")
		db.execute("CREATE TABLE users(id SERIAL primary key unique, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
		db.execute("CREATE TABLE reviews(id SERIAL primary key , users_id INTEGER NOT NULL REFERENCES users,\
			books_isbn VARCHAR NOT NULL REFERENCES books, rating VARCHAR NOT NULL, review VARCHAR NULL)")
		print ("Postgres tables created")

		f=open("books.csv")
		reader= csv.reader(f)
		for isbn,title,author,year in reader:
			if isbn != "isbn":
				db.execute("INSERT INTO books (isbn, title, author, year) VALUES ( :isbn, :title, :author, :year)", 
					{"isbn":isbn, "title":title, "author":author, "year":year})
		db.commit()
		print ("Book data from excel added to postgres tables")
	except:
		print ("Postgres tables already exist, with all the book data")

	return render_template("login.html")
	#return render_template("home.html") 



@app.route("/login", methods=["POST", "GET"])
def index():
	if request.method == "get":
		u1 = ""
	u1 = request.form.get("username")

	session["u1"] = u1 \

	u1 = str(u1).lower()
	p1 = str(request.form.get("password"))

	db.execute("ROLLBACK")
	db.commit()

	u = db.execute("SELECT username FROM users WHERE username=:u1", {"u1":u1})
	u = u.fetchone()
	p = db.execute("SELECT password FROM users WHERE password=:p1", {"p1":p1})
	p = p.fetchone()

	if u != None and p != None:
		u1 = (session.get('u1')).upper()
		return render_template("home.html", u1=u1)

	else:
		return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 402: Invalid Login</h1>"
		

@app.route("/register", methods=["POST", "GET"])
def register():
	if request.method == "GET":
		return "Please access this page from the Home page."
	else:
		return render_template("register.html")


@app.route("/registering", methods=["POST", "GET"])
def registering():

	ru1 = str(request.form.get("rusername")).lower()
	rp1 = request.form.get("rpassword")
	rp2 = request.form.get("repassword")

	db.execute("ROLLBACK")
	db.commit()

	u1 = db.execute("SELECT username FROM users WHERE username=:ru1", {"ru1":ru1})
	u1 = u1.fetchone()


	if ru1 == "" or rp1 == "" or rp2 == "":
		return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 404: Field Missing</h1>"

	elif u1 != None:
		return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 400: Username already exists</h1>"

	elif rp1 != rp2:
		return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 400 Passwords Don't Match</h1>"
	
	else:
		db.execute("INSERT INTO users (username, password) VALUES ( :user, :pass)", {"user":ru1, "pass":rp1})
		db.commit()
		return render_template("login.html")

@app.route("/search1", methods=["POST", "GET"])
def search1():
	u1 = (session.get('u1')).upper()
	return render_template("home.html", u1=u1)


@app.route("/search", methods=["POST", "GET"])
def search():
	
	db.execute("ROLLBACK")
	db.commit()

	#isbn1 = db.execute("SELECT isbn FROM books").fetchall()
	if request.form.get("search") == "":
			return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 404: Book not found.</h1>"

	u1 = (session.get('u1')).upper()
	if u1 == None:
		return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 406: You are not logged in.</h1>"

	if request.form.get("drop") == "isbn":

		isbn = request.form.get("search")
		isbn1 = db.execute("SELECT * FROM books WHERE isbn LIKE '%"+isbn+"%'")
		isbn1 = isbn1.fetchone()  
		if isbn1 != None:
			books = isbn1
			test = db.execute("SELECT * FROM books WHERE isbn LIKE '%"+isbn+"%'").fetchall() 
			#author = db.execute("SELECT author FROM books WHERE isbn=:is", {"is":isbn}).fetchone() 
			return render_template("home.html", books=books, test=test, u1=u1)
		else: 
			return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 404: Book not found.</h1>"

	elif request.form.get("drop") == "title":

		t1 = str(request.form.get("search")).lower()

		t2 = db.execute("SELECT * FROM books WHERE lower(title) LIKE '%"+t1+"%'")
		t2 = t2.fetchone()
		if t2 != None:
			books = t2
			test = db.execute("SELECT * FROM books WHERE lower(title) LIKE '%"+t1+"%'").fetchall()
			return render_template("home.html", books=books, test=test, u1=u1)
		else: 
			return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 404: Book not found.</h1>"

	elif request.form.get("drop") == "author":
 		
		a1 = str(request.form.get("search")).lower()
		
		a2 = db.execute("SELECT * FROM books WHERE lower(author) LIKE '%"+a1+"%'")
		a2 = a2.fetchone()
		if a2 != None:
			books = a2
			test = db.execute("SELECT * FROM books WHERE lower(author) LIKE '%"+a1+"%'").fetchall()
			return render_template("home.html", books=books, test=test, u1=u1)
		else: 
			return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 404: Book not found.</h1>"


@app.route("/review/<string:isbn>",methods=["POST", "GET"])
def review(isbn):

	u1 = session.get('u1')
	
	db.execute("ROLLBACK")
	db.commit()

	if u1 == None:
		return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 406: You are not logged in.</h1>"
	
	uid = db.execute("SELECT id FROM users WHERE username=:uid", {"uid":u1})
	uid = uid.fetchone()
	rate = request.form.get("rate")
	rev = request.form.get("review")
	books = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchall()
	ra = db.execute("SELECT rating FROM reviews WHERE users_id=:uid", {"uid":uid.id})
	ra = ra.fetchone()
	test = books
	u1 = (session.get('u1')).upper()
	reviews = db.execute("SELECT review FROM reviews WHERE books_isbn=:isbn", {"isbn":isbn})
	reviews = reviews.fetchone()
		

	# Goodreads deactivated their api keys in december 2020, this no longer works
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "evpsg1O37kbhNObE9gcUEw", "isbns":isbn})
	avg=res.json()['books'][0]['average_rating']
	count=res.json()['books'][0]['work_ratings_count']

	if  rate == "0":
		return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 404: Rating not found</h1>"
		
	elif rate != "0" and rate != None:
			if reviews == None:
				db.execute("INSERT INTO reviews (users_id, books_isbn, rating, review) VALUES (:uid, :isbn, :rate, :rev)", \
					{"uid":uid.id, "isbn":isbn, "rate":rate, "rev": rev})
				db.commit()
				reviews = db.execute("SELECT review FROM reviews WHERE books_isbn=:isbn", {"isbn":isbn})
				reviews = reviews.fetchone()
			else:
				return "<style>body {background-color:#ff0; text-align: center; margin: 250px;}</style> <h1>Error 400: Review already Exists.</h1>"

	return render_template("book.html", books=books, test=test, u1=u1, avg=avg, count=count, reviews=reviews)
	
		


@app.route("/api/<string:isbn>",methods=["POST", "GET"])
def json(isbn):
			db.execute("ROLLBACK")
			db.commit()

			res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "evpsg1O37kbhNObE9gcUEw", "isbns":isbn})
			print(res.json())
			
			avg=res.json()['books'][0]['average_rating']
			count=res.json()['books'][0]['work_text_reviews_count']

			books = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn})
			books = books.fetchone()

			return render_template("api.json", books=books, avg=avg, count=count)

if __name__=="__main__":
	app.run(debug=True)