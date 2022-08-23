# CS50 - Web Project (Flask, Postgres, Goodreads API)

These are only the main files, the environment set-up that would be requires to run the server would have to be configures separately
There is already a running version of the same online at this link: https://booksreview-api.herokuapp.com/


[Unfortunately, Goodreads has deactivated support of API keys since Dec 2020 and this project no longer works until a certain point]

[However, the logic is still applicable, so if a different book related API was used, this project would still be relevant after some minor changes]


Web Programming with Python and JavaScript

My app opens on the login screen (login.html), where the user can either 'Sign in' or 'Sign up'.

If they do not already have an account they can decide to sign up on the registration page (register.html) where they just have to create a username and enter their password two times. If the username alrady exists, the passwords do not mathch, or simply a field is missed, they will be redirected to an error page informing them of what when wrong. The letter case will not matter for the username, but it would for the passwords.

Upon successuful registration, the user can then login and be directed to the home page (home.html). the page shows the username they are signed in as, an option to log out and a text field to search for a book with a drop down menu. The user can then search for any book through even part of the books ISBN, title or author, provided they chose the correct drop down menu option.

Once submitted, the page will load a table with 4 columns (for isbn, title, author and year respectively) showing all the matches to the users search query.

[From this point onwards, this project is depricated due to the lack of proper data retrieval from Goodreads]

The users then have the option to click on the title of the book itself to be redirected to the book's page (book.html), where they are given the the isbn, title, author and publication year again, but with the inclusion of the average Goodreads rating of the book and the number of people that have rated it. On the same page, the users can also choose to submit their own review of the book. They can either submit a written text with a rating between 1 to 5 stars, or jsut the rating alone without additional text. Once submitted they can see their own review on the page, unique to them, and unable to add another.

Layout.html merely serves as the basic layout, of course, for all the other html pages mentioned. 

Import.py uses the features in python to open, read, and create tables and insert the 5000 rows of data from the books.csv, online to the postgresSQL website. 

Finally, api.json allows the users to submit a GET request on my app directly to get the title, author, publication year, isbn, number of reviews and average rating of any book from just the isbn that would have been submitted. 
