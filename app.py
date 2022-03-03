from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ihin.db'
db = SQLAlchemy(app)

#pythonを対話モードにし、from app import db → db.create_all()でDB作成
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(40), nullable=False)
    user_image_url = db.Column(db.String(120))
    sreated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

@app.route("/")
def hello_world():
    return render_template('index2.html')

@app.route('/create', methods=['GET', 'POST'])
#@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        status = request.form.get('status')
        f = request.files['image']
        filepath = 'static/images/' + secure_filename(f.filename)
        f.save(filepath)
        filepath = '/' + filepath
        post = Post(title=title, category=category, status=status, user_image_url=filepath)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')