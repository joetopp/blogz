from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogstar@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'a;sdlfkjag;aoihq;eonmxxzmqlw193827'

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

    def __repr__(self):
        return '<Title ' + self.title + '>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User ' + self.username + '>'

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_err = ""

        user_real = User.query.filter_by(username=username).first()

        if user_real:
            if user_real.password != password:
                login_err = "Your username and password don't match."
        else:
            login_err = "Invalid username."

        if login_err != "":
            return render_template("login.html",login_err=login_err, username=username)

        #all is well
        session['username'] = username
        return redirect("/newpost")

    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        name_err = ""
        pass_err = ""

        #validate username
        if username == "":
            name_err = "Please enter a username."
        elif len(username) < 3:
            name_err = "Your username must be at least 3 characters."
        elif User.query.filter_by(username=username).first():
            name_err = "That username is already taken."

        #validate password
        if password == "":
            pass_err = "Please enter a password."
        elif len(password) < 3:
            pass_err = "Your password must be at least 3 characters."
        elif password != verify:
            pass_err = "Your passwords don't match."

        #give feedback
        if name_err != "" or pass_err != "":
            return render_template("signup.html", username=username, name_err=name_err, pass_err=pass_err)
        
        #all is well
        newuser = User(username, password)
        db.session.add(newuser)
        db.session.commit()
        session['username'] = username
        print(session)
        return redirect("/newpost")

    return render_template('signup.html')

@app.route("/logout")
def logout():
    del session['username']
    return redirect("/")

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

        author = User.query.filter_by(username=session['username']).first()
        newpost = Blog(title, body, author)
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