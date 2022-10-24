# Importing required libraries
from http import client
from googleplaces import GooglePlaces, types, lang
from flask import Flask, render_template, request, session,redirect,url_for,current_app, g,flash
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from werkzeug.local import LocalProxy
import webbrowser
import bcrypt
import re,requests
import json
import hashlib
import js2py
import socket
import csv 
import pandas as pd
from bson.objectid import ObjectId
from pymongo import MongoClient
mongopass="mongodb+srv://@cluster0.ctbm1h1.mongodb.net/?retryWrites=true&w=majority"
salt="optum"
app = Flask(__name__)
app.config['SECRET_KEY'] = "OPTUM Startathon"
client=MongoClient(mongopass)
db=client.curd
myCollection=db.myColl
doctor=db.doctor
hospital=db.hospital
user=db.user
ambulanceRequest=db.ambulanceRequest
print('myCollection')
print(myCollection)
API_KEY = ''
# https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=27.216502,77.974229&radius=1500&type=hospitale&key=
df = pd.read_csv('disease.csv')
df.to_csv('disease.csv', index=None)

google_places = GooglePlaces(API_KEY)
query_result = google_places.nearby_search(

    lat_lng ={'lat': 27.216502, 'lng': 77.974229},
	radius = 1000,

	types =[types.TYPE_HOSPITAL])
@app.route("/")
def index():
    # query_result = google_places.nearby_search(

    # lat_lng ={'lat': 27.216502, 'lng': 77.974229},
	# radius = 1000,

	# types =[types.TYPE_HOSPITAL])
    # if query_result.has_attributions:
    #     print (query_result.html_attributions)
	   



    for place in query_result.places:
	    print(place)
	    print (place.name)
	    print("Latitude", place.geo_location['lat'])
	    print("Longitude", place.geo_location['lng'])
	    print("Longitude", place.place_id)

        
    lat=27.2199704
    lng=77.97317529999999
    name="Dr. HS Asopa"
    specialization="cardiologist"
    available="yes"
    place_id="ChIJuxt1aH53dDkRe-sf1Y3yAh8"
    myVal={"place_id":place_id,"lat":lat,"lng":lng,"name":name,"specialization":specialization}
    #x=doctor.insert_one(myVal)
    booked=None
    return render_template("index.html",place=query_result.places,booked=booked)

@app.route("/registerUser")
def login():
    return render_template("register.html")




@app.route("/ambulance")
def index2():
    
    return render_template("input.html")

@app.route("/location/<placeid>")
def index1(placeid):
     print("here")
     ambulanceRequest.insert_one({'username': session['username'], 'hospitalId': placeid})
     flash("Successfully Booked",'danger')
     return render_template("index.html",place=query_result.places,booked="Successfully Booked")
     
@app.route("/ok")
def ok():
     session.pop('_flashes', None)
     return render_template("index.html",place=query_result.places,booked='')


# @app.route("/loginUser")
# def loginUser():
#      return render_template("login.html")


# @app.route("/loginUser",methods = ['POST'])
# def logUser():
#     name=request.form['username']
#     pswd=request.form['password']
#     print("check login")
#     pswd=pswd+ salt
#     h = hashlib.md5(pswd.encode())
#     print(h.hexdigest())
#     for x in user.find({ "username": name,"password":h.hexdigest()}):
#         if(x==''):
#             print('empty')
#         print(x)

@app.route('/loginUser', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        signin_user = user.find_one({'username': request.form['username']})
        if signin_user:
         userbytes=request.form['password'].encode('utf-8')
         result = bcrypt.checkpw(userbytes, signin_user['password'])
         
         pass2=signin_user['password']
         print(pass2)
         if result:
                session['username'] = request.form['username']
                return redirect(url_for('index'))

        flash('Username and password combination is wrong')
        return render_template('login.html')

    return render_template('login.html') 


@app.route('/loginHospital', methods=['GET', 'POST'])
def signinHospital():
    if request.method == 'POST':
        signin_user = hospital.find_one({'username': request.form['username']})
        if signin_user:
         userbytes=request.form['password'].encode('utf-8')
         result = bcrypt.checkpw(userbytes, signin_user['password'])
         
         pass2=signin_user['password']
         print(pass2)
         dataz=[]
         if result:
                session['username'] = request.form['username']
                print(signin_user['_id'])
                # for x in doctor.find():
                #     print(x)
                for x in doctor.find({ "hospitalId": str(signin_user['_id'])}):
                #   print("dataz")
                #   print(x)
                  dataz.append(x);
                print(dataz)
                return render_template('hospitalHome.html',dataz=dataz) 

        flash('Username and password combination is wrong')
        return render_template('loginHospital.html')

    return render_template('loginHospital.html') 


@app.route('/registerHospital', methods=['POST', 'GET'])
def regiHospital():
    if request.method == 'GET':
         return render_template('registerHospital.html') 
    elif request.method == 'POST':
        pid=request.form['pid']
        hosName=request.form['hosName']
        name=request.form['username']
        pswd=request.form['password']
        signup_user =hospital.find_one({'username': name})
        if signup_user:
         flash(request.form['username'] + ' username is already exist')
         return redirect(url_for('signup'))
        hashed=pswd.encode('utf-8')
        salt=bcrypt.gensalt()
        hash=bcrypt.hashpw(hashed,salt)
        # hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        hospital.insert_one({'username': request.form['username'],"placeId":pid,"Hospital_Name":hosName, 'password': hash})
        return render_template('loginHospital.html')

    return render_template('registerHospital.html')

@app.route('/registerDoctor')
def regiDoctor():
    if request.method == 'GET':
         return render_template('registerDoctor.html') 
    elif request.method == 'POST':
        print("here i am dodo")
        stri='blog_link'
        specialization=''
        j=0
        while(request.form[stri+str(j)]!=None):
            print(request.form[stri+str(j)])
            specialization+=request.form[stri+str(j)]+','
            j=j+1


        
        print(specialization)
        
        # print(request.form[specialization])
        # print(request.form['blog_link1'])
        uname=request.form['nameDoc']
        print(uname)
        print("here should i")
        name=request.form['username']
        pswd=request.form['password']
        hid=request.form['hospoitalID']
        signup_user =hospital.find_one({'username': name})
        if signup_user:
         flash(request.form['username'] + ' username is already exist')
         return render_template('registerDoctor.html')
        hashed=pswd.encode('utf-8')
        salt=bcrypt.gensalt()
        hash=bcrypt.hashpw(hashed,salt)
        # hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        doctor.insert_one({'hospitalId':hid,'name':uname,'username': request.form['username'], 'password': hash,'available':'yes'})
        return render_template('loginDoctor.html')

    return render_template('registerDoctor.html')

@app.route('/doctorconfirm/<id>', methods=['POST'])
def doctorConfirm(id):
     print("gotcha")
     print(request.form['fav'])
     ans=request.form['fav']
     myquery = { "_id": ObjectId(id) }
     newvalues = { "$set": { "available":ans } }
     doctor.update_one(myquery, newvalues)
     print("Yay")
     return render_template('doctorHome.html',avl='no',id=id) 

@app.route('/registerDoctor/<prm>', methods=['POST'])
def regiDoctor1(prm):
        print("here i am")
        stri='blog_link'
        specialization=''
        j=0

        while(j<int(prm)):
            print(request.form[stri+str(j)])
            specialization+=request.form[stri+str(j)]+','
            j=j+1


        
        print(specialization)
        uname=request.form['nameDoc']
        print(uname)
        # print(request.form[specialization])
        # print(request.form['blog_link1'])
        name=request.form['username']
        pswd=request.form['password']
        hid=request.form['hospoitalID']
        signup_user =hospital.find_one({'username': name})
        if signup_user:
         flash(request.form['username'] + ' username is already exist')
         return render_template('registerDoctor.html')
        hashed=pswd.encode('utf-8')
        salt=bcrypt.gensalt()
        hash=bcrypt.hashpw(hashed,salt)
        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        doctor.insert_one({'hospitalId':hid,'name':uname,'username': request.form['username'], 'password': hash,'specialization':specialization,"available":'yes'})
        return render_template('loginDoctor.html')



@app.route('/registerUser', methods=['POST', 'GET']) 
def signup():
   if request.method == 'POST':
    print("herr")
    name=request.form['username']
    pswd=request.form['password']
    signup_user = user.find_one({'username': name})
    if signup_user:
        flash(request.form['username'] + ' username is already exist')
        return redirect(url_for('signup'))
    hashed=pswd.encode('utf-8')
    salt=bcrypt.gensalt()
    hash=bcrypt.hashpw(hashed,salt)
    # hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
    user.insert_one({'username': request.form['username'], 'password': hash})
    return redirect(url_for('signin'))

   return render_template('signup.html')



@app.route('/data',methods = ['POST'])  
def data(): 
    place_id="ChIJuxt1aH53dDkRe-sf1Y3yAh8"
#     Latitude 27.2148962
# Longitude 77.9782149 
    # lat=27.2148962
    # lng=77.9782149
    inp=request.form['data'] 
    hosid=request.form['hosid'] 
    print(inp)
    all_doc=[]
    data = pd.read_csv('disease.csv')
    with open('disease.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        print(data)
    for i in data:
     if i[1]==inp:
         y=i[2].split(',')
         break
    print(y)
    for row in y:
        print(row)
        for x in doctor.find({ "hospitalId": hosid, "specialization":row}):
            print("data")
            print(x)
            all_doc.append(x);
    print("all_doc")
    print(all_doc)
    for x in doctor.find({ "hospitalId": hosid}):
            print("dataziez")
            print(x)
            print(x['name'])
            sp = x['specialization'].split(", ")
            print("spliting")
            for i in sp:
                i=i[:-1]
                if(i==row):
                    all_doc.append(x);
    return render_template("doc.html",doc=all_doc[0])
    #for x in doctor.find({},{ "lat": lat, "lng": lng, "specialization": }):
    #  x=i[2].split(',')
    #  mp[i[1]]=x
    # print(mp)

@app.route('/loginDoctor', methods=['GET', 'POST'])
def loginDoctor():
    if request.method == 'POST':
        signin_user = doctor.find_one({'username': request.form['username']})
        print(signin_user)
        if signin_user:
         userbytes=request.form['password'].encode('utf-8')
         result = bcrypt.checkpw(userbytes, signin_user['password'])
         
         pass2=signin_user['password']
         print(pass2)
         if result:
                session['username'] = request.form['username']
                print(str(signin_user['_id']))
                return redirect("/doctor/home/"+str(signin_user['_id'])) 

        flash('Username and password combination is wrong')
        return render_template('loginDoctor.html')

    return render_template('loginDoctor.html') 

@app.get('/doctor/home/<idOfDoctor>')
def doctorHome(idOfDoctor):
    for x in doctor.find({ "_id": ObjectId(idOfDoctor)}):
            print("data")
            print(x['available'])
            return render_template('doctorHome.html',avl=x['available'],id=idOfDoctor) 



if __name__ == "__main__":
 app.run( port=10000)


