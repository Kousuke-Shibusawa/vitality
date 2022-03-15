from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from datetime import datetime
import pytz
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ihin.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

#pythonを対話モードにし、from app import db → db.create_all()でDB作成
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(40), nullable=False)
    user_image_url = db.Column(db.String(120))
    sreated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    useaddress = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(12))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        user = User.query.all()
        return render_template('index.html', posts=posts)

@app.route("/dispose", methods=['GET', 'POST'])
@login_required
def index2():
    if request.method == 'GET':
        posts = Post.query.all()
        user = User.query.all()
        return render_template('index2.html', posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        useaddress = request.form.get('useaddress')
        password = request.form.get('password')
        user = User(username=username, useaddress=useaddress, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        useaddress = request.form.get('useaddress')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        user = User.query.filter_by(useaddress=useaddress).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            return redirect('/loginerror')
    else:
        return render_template('login.html')

@app.route('/loginerror')
def loginerror():
    return render_template('loginerror.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        status = request.form.get('status')
        username = request.form.get('username')
        f = request.files['image']
        filepath = 'static/images/' + secure_filename(f.filename)
        f.save(filepath)
        filepath = '/' + filepath
        post = Post(title=title, category=category, status=status, username=username, user_image_url=filepath)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.category = request.form.get('category')
        post.status = request.form.get('status')
        f = request.files['image']
        filepath = 'static/images/' + secure_filename(f.filename)
        f.save(filepath)
        filepath = '/' + filepath
        post.user_image_url = filepath
        db.session.commit()
        return redirect('/')

@app.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')