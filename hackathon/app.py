# importing flask
import importlib
from smtplib import quotedata
# from threading import get_ident
from turtle import right
from flask import Flask, render_template, request, session,redirect,url_for
from numpy import insert
import csv
import random
import pandas as pd
from requests import Session

# importing pandas module
import pandas as pd


app = Flask(__name__)


# reading the data in the csv file
df = pd.read_csv('disease.csv')
df.to_csv('disease.csv', index=None)


# route to html page - "table"
@app.route('/')
@app.route('/table')
def table():
#  session['data']={}
 mp={}
 data = pd.read_csv('disease.csv')
 with open('disease.csv', newline='') as csvfile:
     data = list(csv.reader(csvfile))
 print(data)
 print("abdu")
 for i in data:
     x=i[2].split(',')
     mp[i[1]]=x
 print(mp)
 return render_template('homepage.html')
	
if __name__ == "__main__":
	app.run(host="localhost", port=int("10000"))
