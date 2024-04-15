import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["book"]  # Use the "book" database
collection = db["allbook"]  # Use the "allbook" collection


@app.route("/")
def home():
    """Home page route."""
    return render_template("index.html")


@app.route("/books")
def list_books():
    """List all books route."""
    books = list(collection.find())  # Retrieve all books from the database
    return render_template("books.html", books=books)


@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    """Add a new book route."""
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]
        if title and author and year:
            book = {"title": title, "author": author, "year": int(year)}
            collection.insert_one(book)
            flash("Book added successfully!", "success")
            return redirect(url_for("list_books"))
        else:
            flash("Please fill in all fields!", "error")
    return render_template("add_book.html")


@app.route("/books/edit/<string:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    """Edit an existing book route."""
    book = collection.find_one({"_id": book_id})
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]
        if title and author and year:
            update_book = {"title": title, "author": author, "year": int(year)}
            collection.update_one({"_id": book_id}, {"$set": update_book})
            flash("Book updated successfully!", "success")
            return redirect(url_for("list_books"))
        else:
            flash("Please fill in all fields!", "error")
    return render_template("edit_book.html", book=book)


@app.route("/books/delete/<string:book_id>", methods=["GET", "POST"])
def delete_book(book_id):
    """Delete a book route."""
    if request.method == "POST":
        collection.delete_one({"_id": book_id})
        flash("Book deleted successfully!", "success")
        return redirect(url_for("list_books"))
    return render_template("delete_book.html", book_id=book_id)


if __name__ == "__main__":
    app.run(debug=True)
