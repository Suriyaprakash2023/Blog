from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
#from blog import db,login_manager

from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,TextAreaField,PasswordField,SubmitField,BooleanField,validators,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError#,FileAllowed
#from blog.models import User
from flask_login import UserMixin
#from blog import db,login_manager


#from blog.models import User
import sys
sys.path.append('D:\Flask\Flask-blog')


app=Flask(__name__)

app.config['SECRET_KEY']="e5678910bcsmcdfq8977iyh"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'

db=SQLAlchemy(app)
app.app_context().push()


with app.app_context():
    db.create_all()
    
from flaskblog import routes