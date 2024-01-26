from wtforms import StringField,TextAreaField,PasswordField,SubmitField,BooleanField,validators,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError#,FileAllowed
from flask_wtf import FlaskForm
from flask_wtf import Form
from flask_wtf.file import FileField,FileAllowed
from . import app
from . import db
from .models import Post,User


class Registrationform(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=4, max=20)],render_kw={"placeholder":"Username"})
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder":"Email"})
    password=PasswordField("Password",validators=[DataRequired(),Length(min=6)],render_kw={"placeholder":"Password"})
    confirmpassword=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder":"Confirm Password"})
    submit=SubmitField("Sing up")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Alredy Exists...Please use a diffrent username..!")


    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email address Alredy Registered with us...Please Login with the Password.!!")


class Loginform(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder":"Email"})
    password=PasswordField("Password",validators=[DataRequired(),Length(min=6)],render_kw={"placeholder":"Password"})
    remember=BooleanField("Remember Me")
    submit=SubmitField('Login')


class Updateform(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=4, max=20)],render_kw={"placeholder":"Username"})
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder":"Email"})
    #picture = FileFiled("Update profile Picture",validators=[FileAllowed(['jpg','jpeg','png'])])
    submit=SubmitField("Update")

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username Alredy Exists...Please use a diffrent username..!")


    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email address Alredy Registered with us...Please Login with the Password.!!")

class Postform(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content=TextAreaField("Content",validators=[DataRequired()])
    submit=SubmitField('Post')

class ResetRequestform(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request Reset Password')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("his Email is not Registered with us. Please Register to the system if you have not registered.!!")
class ResetPasswordform(FlaskForm):
    password=PasswordField("Password",validators=[DataRequired(),Length(min=6)],render_kw={"placeholder":"Password"})
    confirmpassword=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder":"Confirm Password"})
    submit=SubmitField("Reset")

with app.app_context():
    db.create_all()