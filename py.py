import os
import requests


from flask import Flask, session,render_template,request,redirect,url_for,Markup
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "evpsg1O37kbhNObE9gcUEw", "isbns": "0439023483"})
print(res.json())

   "review_count": 28,
    "average_score": 5.0

def bob():
    global me
    me = "locally defined"   # Defined locally but declared as global
    print (me)

bob()
print (me)