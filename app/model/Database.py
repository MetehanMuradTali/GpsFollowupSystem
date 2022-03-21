import datetime
from flask import session,Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

import os

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
def create_app():
    app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'deneme.sqlite')
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    cars =  db.relationship('User_Cars', backref='user', lazy=True)

    def __init__(self,username,password):
        self.username = username
        self.password = password

class UserLoginLogout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    login_date = db.Column(db.String(80), nullable=False)
    logout_date = db.Column(db.String(80))

    def __init__(self,login_date,username):
        self.login_date = login_date
        self.username=username
        self.logout_date = None

class User_Cars(db.Model):
    cars_id = db.Column(db.Integer, unique=True, nullable=False,primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __init__(self,cars_id,person_id):
        self.cars_id = card_id
        self.person_id = person_id

def CreateUser():
    user = viewcontroller.views.User(username="deneme1",password="deneme1")
    db.session.add(user)
    db.session.commit()

def SearchUser(username,password):
        kullanıcı=User.query.filter_by(username=username, password=password).first()
        if kullanıcı is None:
            return False
        else:
            return True

def CalculateTime():
    datetime_object = datetime.datetime.now()
    return datetime_object.strftime("%c")


def PostLoginTime():
    time = UserLoginLogout(login_date=session.get("logindate"),username=session.get("username"))
    db.session.add(time)
    db.session.commit()

def PostLogoutTime():
    time = UserLoginLogout.query.filter_by(login_date=session.get("logindate"),username=session.get("username")).first()
    setattr(time, "logout_date", CalculateTime())
    db.session.commit()
    session.pop("username", None)
    session.pop("logindate",None)

def GetCarIds():
    kullanıcı_id=User.query.filter_by(username=session.get("username")).first().id
    cars=User_Cars.query.filter_by(person_id=kullanıcı_id).all()
    cars_id=[]
    for car in cars:
        cars_id.append(car.cars_id)
    return cars_id

