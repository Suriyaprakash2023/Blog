from . import db 
from . import app 
from datetime import datetime
from flask_login import UserMixin
#from blog import db,login_manager
from flask_bcrypt import Bcrypt






class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=True,unique=True)
    email=db.Column(db.String(90),nullable=True,unique=True)
    password=db.Column(db.String(8),nullable=True)
    image_field=db.Column(db.String(20),nullable=True,default='default.jpg')
    
    posts=db.relationship('Post',backref='author',lazy=True)

    def get_reset_tocken(self,expires_sec=1800):
        s=Serializer(app.config['SECRECT_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    @staticmethod
    def verify_rest_token(token):
        s=Serializer(app.config['SECRECT_KEY'])
        try:
            user_id =s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



    def __repr__(self):
        return f"User{'{self.username}','{self.email}','{self.image_field}'}"
    
   
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    content=db.Column(db.Text,nullable=False)

    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)

    def __repr__(self):
        return f"Post{'{self.title}','{self.date_posted}'}"

with app.app_context():
    db.create_all()

