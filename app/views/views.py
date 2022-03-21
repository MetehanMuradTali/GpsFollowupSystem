from flask import Flask,render_template,request,redirect,url_for,session
import app.model as databasecontroller
import datetime
from app.model import create_app
import os
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta

app = create_app()
app.secret_key = "hello"
sio = SocketIO(app)


@app.route("/userlogin",methods=['POST','GET'])
def Login():
    if not "username" in session:
        if request.method == 'POST':
            username=request.form.get("username")
            password=request.form.get("password")
            if session.get('attempt') > 0:
                if databasecontroller.SearchUser(username, password):
                    session["username"] = username
                    session["logindate"] = databasecontroller.CalculateTime()
                    databasecontroller.PostLoginTime()
                    return redirect(url_for("MainMenu"))
                else:
                    attempt = session.get('attempt')
                    attempt -= 1
                    session['attempt'] = attempt
                    print(session.get('attempt'))
                    return render_template("login.html")
            else :
                return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        return redirect(url_for("MainMenu"))



@app.route("/mainmenu",methods=['POST','GET'])
def MainMenu():
    session['attempt'] = 2
    if request.method == 'GET':
        if "username" in session:
            username=session.get("username")
            cars=databasecontroller.GetCarIds()
            return render_template("mainmenu.html",username=username,cars=cars)
        else:
            return redirect(url_for("Login"))
    else:
        if request.form['action'] == 'Logout':
            databasecontroller.PostLogoutTime()
            return redirect(url_for("Login"))

@sio.on('connect')
def connect_message():
    emit('Connected', {'data': 'yeni kullanici baglandi'})

@sio.on('Request')
def deneme(data):
    query=databasecontroller.SearchCoordinates(data.get('car_id'),data.get('firstdate').replace("T"," "),data.get('seconddate').replace("T"," "))
    emit('Answer',query)


@sio.on('Requests')
def deneme(data):
    query1=databasecontroller.SearchCoordinates(data.get('car_id1'),data.get('firstdate1').replace("T"," "),data.get('seconddate1').replace("T"," "))
    query2=databasecontroller.SearchCoordinates(data.get('car_id2'),data.get('firstdate2').replace("T"," "),data.get('seconddate2').replace("T"," "))
    emit('Answers', {'query1':query1,'query2':query2})

@sio.on('RequestLoad')
def deneme():
    cars = databasecontroller.GetCarIds()
    car1=cars[0]
    car2=cars[1]
    query1=databasecontroller.theLastCoordinate(car1)
    query2=databasecontroller.theLastCoordinate(car2)
    emit('Load',{'query1':query1,'query2':query2})

@sio.on('ReqLastCoordinate')
def deneme(data):
    query=databasecontroller.theLastCoordinate(data)
    emit('SendLastCoordinate',query)

if __name__ == "__main__" :
 sio.run(app)



