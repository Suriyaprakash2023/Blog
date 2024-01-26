from flask import render_template,redirect,request,url_for,flash
from . import db
from . import app
from flaskblog.models import User,Post
from flask_login import LoginManager,login_user,current_user,logout_user,login_required
from datetime import datetime 
from .form import *
from flask_bcrypt import Bcrypt

bcrypt= Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view='login'
#login_manager.init_app(app)
login_manager.login_massage_category = 'info'

 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
@app.route('/index')
def home():
    posts = Post.query.all() 
    return render_template('index.html', posts=posts)

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/about')
def end():
    return render_template('about.html',title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=Registrationform()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your Account has been Created Successfully..Now You Login")
        return redirect(url_for('home'))
    return render_template('register.html',form=form,title="Register")

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=Loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash(f'Welcome {User.username}','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('login unsuccessful..Please Check your Credentials','danger')

    return render_template('login.html', form=form , title="Login")
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.tocken_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    op_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(op_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account',methods=['POST','GET'])
@login_required
def account():
    form=Updateform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Your Details have been Updated..!!",'success')
        return redirect(url_for('account'))
    elif request.method =="GET":
        form.username.data = current_user.username
        form.email.data=current_user.email

    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    form= Updateform()
    return render_template('account.html',title="Account", image_file=image_file,form=form)

@app.route('/post/new',methods=['POST','GET'])
@login_required
def new_post():
    form=Postform()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been successfully Created !!",'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title="Create Post",form=form,legend='New Post')


@app.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@app.route('/post/<int:post_id>/update',methods=['POST','GET'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user :
        abort(403)
    form = Postform()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your Post has been Updated.!!','success')
        return redirect(url_for('post',post_id=post.id))
    form.title.data=post.title
    form.content.data=post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Upadte Post')

@app.route('/post/<int:post_id>/delete',methods=['POST','GET'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user :
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been Deleted.!!','success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token=user.get_reset_token()
    form=ResetRequestform()
    with open('D:\Flask\Blog\password.txt','r') as f:
        password=f.read()
        f.close()
    msge1=list({url_for('reset_token',token=token,_external=True)})
    msge=msge1[0]
    msg=MIMEText(msge)

    me="suriyakannan@gmail.com"
    you=form.email.data
    msg['Subject']="password Reset Email for the Flask Blog Account"
    msg['Form']=me
    msg['To']=you

    s=smtplib.SMTP('smtp.gamil.com',587)
    s.starttls()
    s.login(me,password)
    s.send_message(msg)
    s.quit()

@app.route('/reset_password',methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=ResetRequestform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Password Reset has been sent to Your Registered Email','success')
        return redirect('login')
    return render_template('reset_request.html',title='Reset Password',form=form)

@app.route('/reset_password/<token>',methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user=User.verify_reset_tocken(token)
    if user is None:
        flash('This is an invalid token or it might have expired..!','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordform()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data)
        user.password=hashed_pw
        db.session.commit()
        flash('Your Password has been Successfully..!!!','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password',form=form)
