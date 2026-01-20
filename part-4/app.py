from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # allow JS to fetch from local frontend

app = Flask(__name__)
CORS(app)  # allow all origins, optional for local testing

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ MODELS ------------------

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    return jsonify({"message": "Library API running"}), 200

# --------- AUTHORS ---------
@app.route('/api/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    result = []
    for a in authors:
        result.append({
            "id": a.id,
            "name": a.name,
            "email": a.email,
            "books": [{"id": b.id, "title": b.title, "year": b.year} for b in a.books]
        })
    return jsonify(result), 200

@app.route('/api/authors/<int:id>', methods=['GET'])
def get_author(id):
    a = Author.query.get_or_404(id)
    return jsonify({
        "id": a.id,
        "name": a.name,
        "email": a.email,
        "books": [{"id": b.id, "title": b.title, "year": b.year} for b in a.books]
    }), 200

@app.route('/api/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        return jsonify({"error": "Name and Email required"}), 400
    new_author = Author(name=data['name'], email=data['email'])
    db.session.add(new_author)
    db.session.commit()
    return jsonify({"message": "Author created", "id": new_author.id}), 201

@app.route('/api/authors/<int:id>', methods=['PUT'])
def update_author(id):
    author = Author.query.get_or_404(id)
    data = request.get_json()
    author.name = data.get('name', author.name)
    author.email = data.get('email', author.email)
    db.session.commit()
    return jsonify({"message": "Author updated"}), 200

@app.route('/api/authors/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": "Author deleted"}), 200

# --------- BOOKS ---------
@app.route('/api/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    query = Book.query

    # sorting logic
    if hasattr(Book, sort):
        column = getattr(Book, sort)
        if order == 'desc':
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    books = []
    for b in pagination.items:
        books.append({
            "id": b.id,
            "title": b.title,
            "year": b.year,
            "author": {
                "id": b.author.id,
                "name": b.author.name
            } if b.author else None
        })

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total_books": pagination.total,
        "total_pages": pagination.pages,
        "sort": sort,
        "order": order,
        "books": books
    }), 200


@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    b = Book.query.get_or_404(id)
    return jsonify({
        "id": b.id,
        "title": b.title,
        "year": b.year,
        "author": {"id": b.author.id, "name": b.author.name} if b.author else None
    }), 200

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data.get('title') or not data.get('author_id'):
        return jsonify({"error": "Title and Author required"}), 400
    author = Author.query.get(data['author_id'])
    if not author:
        return jsonify({"error": "Author not found"}), 404
    new_book = Book(title=data['title'], year=data.get('year'), author_id=author.id)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created", "id": new_book.id}), 201

@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.year = data.get('year', book.year)
    author_id = data.get('author_id')
    if author_id:
        author = Author.query.get(author_id)
        if not author:
            return jsonify({"error": "Author not found"}), 404
        book.author_id = author.id
    db.session.commit()
    return jsonify({"message": "Book updated"}), 200

@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

# ------------------ RUN ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates tables safely inside app context
    app.run(debug=True)
