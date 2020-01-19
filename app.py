import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'reading_list'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')


mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def get_home():
    return render_template('index.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


@app.route('/get_books')
def get_books():
    return render_template("books.html", books=mongo.db.books.find())


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    all_genres = mongo.db.genres.find()
    return render_template("editbooks.html", book=the_book,
                           genres=all_genres)


@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    books = mongo.db.books
    books.update(
        {'_id': ObjectId(book_id)},
        {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'genre_name': request.form.get('genre_name'),
            'series': request.form.get('series'),
            'published': request.form.get('published'),
            'amazon': request.form.get('amazon'),
            'description': request.form.get('description'),
            'picture': request.form.get('picture')
        }
    )
    return redirect(url_for('get_books'))


@app.route('/add_book')
def add_book():
    return render_template('addbook.html', books=mongo.db.books.find(),
                           genres=mongo.db.genres.find())


@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    new_book = request.form.to_dict()
    new_book['user_id'] = 'userid'
    books.insert_one(request.form.to_dict())
    return redirect(url_for('get_books'))


@app.route('/book/<book_id>')
def book(book_id):
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("per_book.html", book=the_book)


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('get_books'))


@app.route('/books_per_genre')
def get_books_per_genre():
    return render_template('genres.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


@app.route('/get_registered')
def get_registered():
    return render_template('register.html', users=mongo.db.users.find())


@app.route('/insert_user', methods=['POST'])
def insert_user():
    users = mongo.db.users
    users.insert_one(request.form.to_dict())
    return redirect(url_for('get_users'))


@app.route('/login')
def login():
    return render_template('login.html', users=mongo.db.users.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
