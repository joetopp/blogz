from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogstar@localhost:8889/blogz'
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
        titleerr = ""
        bodyerr = ""

        if title == "":
            titleerr = "Please fill in the title"

        if body == "":
            bodyerr = "Please fill in the body"

        if titleerr != "" or bodyerr != "":
            return render_template("newpost.html", titleerr=titleerr, bodyerr=bodyerr)

        newpost = Blog(title, body)
        db.session.add(newpost)
        db.session.commit()
        return redirect("/blog?id=" + str(newpost.id))

    return render_template('newpost.html')

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    postid = request.args.get("id")
    if postid:
        post = Blog.query.filter_by(id=int(postid)).first()
        return render_template('post.html', title=post.title, body=post.body)

    bloglist = Blog.query.all()
    return render_template('blog.html', bloglist=bloglist)

@app.route("/")
def index():
    return redirect("/blog")

if __name__ == "__main__":  
    app.run()