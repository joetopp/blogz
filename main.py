from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:joetopp@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Title ' + self.title + '>'

@app.route("/newpost", methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        newpost = Blog(title, body)
        db.session.add(newpost)
        db.session.commit()
        
    return render_template('newpost.html')

@app.route("/blog", methods=['GET', 'POST'])
def blog():

    bloglist = Blog.query.all()
    return render_template('blog.html', bloglist=bloglist)

if __name__ == "__main__":  
    app.run()