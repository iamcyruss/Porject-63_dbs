from flask_sqlalchemy import SQLAlchemy
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


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = book.query.get(book_id)
    return render_template("edit.html", book_rating=book_selected)


@app.route("/delete")
def delete():
    book_to_delete = request.args.get('id')
    book.query.filter(book.id == book_to_delete).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()
