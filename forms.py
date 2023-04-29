from flask_wtf import Form

from wtforms import TextField, BooleanField
from wtforms.validators import Required
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, validators, ValidationError ,SubmitField

class Query(FlaskForm):
    name = TextField('Name'  , [validators.Required("Please enter your name.")])
    email = TextField('Email' ,  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = TextField('Subject' ,  [validators.Required("Please enter a subject.")])
    query = TextAreaField('Query' ,  [validators.Required("Please enter your Query.")])
    submit = SubmitField('Submit')

