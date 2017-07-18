from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField,SubmitField
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'derp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(64))  
    content = db.Column(db.String(512))

    def __init__(self,title,content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "Post %r, titled %r" % (self.id, self.title)
class NewForm(FlaskForm):
    title = TextField("title")
    content = TextAreaField("content")
    submit = SubmitField("Send")

@app.route('/')
def index():
    return render_template('pages/index.html', posts = Post.query.all())

@app.route('/new',methods = ['POST', 'GET'])
def new():
    if request.method == 'POST':
        new = Post(request.form.getlist('title')[0],request.form.getlist('content')[0])
        db.session.add(new)
        db.session.commit()
        print(request.form.getlist('title')[0])
        return redirect('/')
    else:
        form = NewForm()
        return render_template('pages/new.html', form=form)

@app.route('/post/<id>')
def show(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('pages/show.html', post=post)

if __name__ == '__main__':
    app.run()