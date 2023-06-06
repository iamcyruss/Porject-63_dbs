from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import Flask, render_template, request, redirect, url_for

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-db.db'
db.init_app(app)

all_books = []


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)


class book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float(), nullable=False)


@app.route('/')
def home():
    return render_template("index.html", books=book.query.all())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        all_books.append(new_book)
        sql = book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(sql)
        db.session.commit()
        
        #NOTE: You can use the redirect method from flask to redirect to another route 
        # e.g. in this case to the home page after the form has been submitted.
        return redirect(url_for('home'))
      
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()
