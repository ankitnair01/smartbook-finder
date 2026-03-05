# User → Flask App → Google Books API → Return Data → Render HTML
''' Backend: Python + Flask
Database: SQLite
Frontend: HTML + Bootstrap + Vanilla JS
API Integration: Google Books API
Deployment: Render

User
 ↓
AJAX Request
 ↓
Flask Backend
 ├── /search  → Calls Google Books API
 ├── /favorites → Stores in SQLite
 ├── /api/books → REST endpoint
 ↓
JSON Response
 ↓
Frontend renders dynamically '''

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# model
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    preview_link = db.Column(db.String(500))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search')
def search():

    query = request.args.get('q', '')

    if not query:
        return jsonify([])

    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    response = requests.get(url)
    data = response.json()
    print(data)

    books = []

    if "items" in data:
        for item in data["items"]:

            info = item.get("volumeInfo", {})

            image_links = info.get("imageLinks", {})

            books.append({
                "title": info.get("title", "No Title"),
                "authors": ", ".join(info.get("authors", ["Unknown Author"])),
                "publishedDate": info.get("publishedDate", "N/A"),
                "thumbnail": image_links.get("thumbnail"),
                "previewLink": info.get("previewLink", "#")
            })

    return jsonify(books)


if __name__ == "__main__":
    app.run(debug=True)

#Google Books Api used