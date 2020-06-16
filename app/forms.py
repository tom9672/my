from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User
import praw

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class addQuestionFrom(FlaskForm):
    question = TextAreaField('Question')
    answer = TextAreaField('Answer')
    submit = SubmitField('Add Question')

class Quiz(FlaskForm):
    #question = TextAreaField('Question')
    answer = TextAreaField('Your Answer')
    submit = SubmitField('Submit Answer')

class doQuizFrom(FlaskForm):
    #question = TextAreaField('Question')
    useranswer = TextAreaField('Your Answer')
    submit = SubmitField('Submit Answer')

class makeQuiz(FlaskForm):
    #question = TextAreaField('Question')
    #answer = TextAreaField('Your Answer')
    submit = SubmitField('Submit Answer')