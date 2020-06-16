from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Create User table in the database
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    quizset_did = db.relationship('QuizSet', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    
#Create Question table
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)

    def __repr__(self):
        return '<Question {}>'.format(self.question)

#Create Question QuizSet
class QuizSet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    useranswer = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    release = db.Column(db.Boolean)
    completed_by_user = db.Column(db.Text)
    #marked = db.Column(db.Boolean)
    #score = db.Column(db.Integer)
    #feedback = db.Column(db.Text)

class QuizSetList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quzisetid = db.Column(db.Integer)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    useranswer = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    release = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)
    marked = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))