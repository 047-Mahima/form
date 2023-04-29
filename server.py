from flask import Flask , render_template , request ,url_for
from forms import Query
from flask_mail import Mail , Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hardtoguess'
app.config['SQLALCHEMY_DATABASE_URI']   =  'sqlite:///' + os.path.join(basedir , 'data.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] =os.environ.get('MAIL_PASSWORD')

app.config['MAIL_SUBJECT_PREFIX'] = '[FLASK APP]'
app.config['MAIL_SENDER'] = 'ADMIN <akashpawar080808@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')


db=SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app,db)

def send_mail_async(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to,subject,template,**kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['MAIL_SENDER'], recipients = [to] )
    msg.body = render_template (template + '.txt',**kwargs)
    msg.html = render_template (template + '.html',**kwargs)
    mail.send(msg)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer , primary_key=True)
  name = db.Column(db.String(50), nullable=False , unique=True)
  email = db.Column(db.String(50) , nullable=False , unique = True)
  subject =  db.Column(db.String(50) , nullable=False)
  query =  db.Column(db.String(500) , nullable=False)
  def __repr__(self):
    return '< User %r>' % self.username


@app.route('/')
def home():
  return render_template('contact.html' , var = 'Mahima')


@app.route('/query',methods=['GET','POST'])
def query():
    form = Query()
    if form.validate_on_submit():
        user = User(name=form.name.data,email=form.email.data,subject=form.subject.data,query=form.query.data)
        db.session.add(user)
        db.session.commit()
        send_mail(user.subject,app.config['ADMIN'],'mail/new_user',user=user)
        flash('Thank You for Your feed back!!!')
    return render_template('query.html',form=form)


if __name__=='__main__':
  app.run()