
# """
# Part 4: REST API with Flask
# ===========================
# Build a JSON API for database operations (used by frontend apps, mobile apps, etc.)

# What You'll Learn:
# - REST API concepts (GET, POST, PUT, DELETE)
# - JSON responses with jsonify
# - API error handling
# - Status codes
# - Testing APIs with curl or Postman

# Prerequisites: Complete part-3 (SQLAlchemy)
# """

# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_demo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# # =============================================================================
# # MODELS
# # =============================================================================

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     year = db.Column(db.Integer)
#     isbn = db.Column(db.String(20), unique=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):  # Convert model to dictionary for JSON response
#         return {
#             'id': self.id,
#             'title': self.title,
#             'author': self.author,
#             'year': self.year,
#             'isbn': self.isbn,
#             'created_at': self.created_at.isoformat() if self.created_at else None
#         }


# ##----------------AUTHOR TABLE------------------
# class Author(db.Model):
#     A_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     city = db.Column(db.String(100), nullable=False)
#     bio = db.Column(db.String(20), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):  # Convert model to dictionary for JSON response
#         return {
#             'A_id': self.A_id,
#             'name': self.name,
#             'city': self.city,
#             'bio': self.bio,
#             'created_at': self.created_at.isoformat() if self.created_at else None
#         }


# # =============================================================================
# # REST API ROUTES
# # =============================================================================

# # GET /api/books - Get all books
# @app.route('/api/books', methods=['GET'])
# def get_books():
#     books = Book.query.all()
#     return jsonify({  # Return JSON response
#         'success': True,
#         'count': len(books),
#         'books': [book.to_dict() for book in books]  # List comprehension to convert all
#     })


# # GET /api/books/<id> - Get single book
# @app.route('/api/books/<int:id>', methods=['GET'])
# def get_book(id):
#     book = Book.query.get(id)

#     if not book:
#         return jsonify({
#             'success': False,
#             'error': 'Book not found'
#         }), 404  # Return 404 status code

#     return jsonify({
#         'success': True,
#         'book': book.to_dict()
#     })


# # POST /api/books - Create new book
# @app.route('/api/books', methods=['POST'])
# def create_book():
#     data = request.get_json()  # Get JSON data from request body

#     # Validation
#     if not data:
#         return jsonify({'success': False, 'error': 'No data provided'}), 400

#     if not data.get('title') or not data.get('author'):
#         return jsonify({'success': False, 'error': 'Title and author are required'}), 400

#     # Check for duplicate ISBN
#     if data.get('isbn'):
#         existing = Book.query.filter_by(isbn=data['isbn']).first()
#         if existing:
#             return jsonify({'success': False, 'error': 'ISBN already exists'}), 400

#     # Create book
#     new_book = Book(
#         title=data['title'],
#         author=data['author'],
#         year=data.get('year'),  # Optional field
#         isbn=data.get('isbn')
#     )

#     db.session.add(new_book)
#     db.session.commit()

#     return jsonify({
#         'success': True,
#         'message': 'Book created successfully',
#         'book': new_book.to_dict()
#     }), 201  # 201 = Created


# # PUT /api/books/<id> - Update book
# @app.route('/api/books/<int:id>', methods=['PUT'])
# def update_book(id):
#     book = Book.query.get(id)

#     if not book:
#         return jsonify({'success': False, 'error': 'Book not found'}), 404

#     data = request.get_json()

#     if not data:
#         return jsonify({'success': False, 'error': 'No data provided'}), 400

#     # Update fields if provided
#     if 'title' in data:
#         book.title = data['title']
#     if 'author' in data:
#         book.author = data['author']
#     if 'year' in data:
#         book.year = data['year']
#     if 'isbn' in data:
#         book.isbn = data['isbn']

#     db.session.commit()

#     return jsonify({
#         'success': True,
#         'message': 'Book updated successfully',
#         'book': book.to_dict()
#     })


# # DELETE /api/books/<id> - Delete book
# @app.route('/api/books/<int:id>', methods=['DELETE'])
# def delete_book(id):
#     book = Book.query.get(id)

#     if not book:
#         return jsonify({'success': False, 'error': 'Book not found'}), 404

#     db.session.delete(book)
#     db.session.commit()

#     return jsonify({
#         'success': True,
#         'message': 'Book deleted successfully'
#     })




# # =============================================================================
# # REST API ROUTES for Author 
# # =============================================================================

# # GET /api/author- Get all author
# @app.route('/api/authors', methods=['GET'])
# def get_authors():
#     authors = Author.query.all()
#     return jsonify({  # Return JSON response
#         'success': True,
#         'count': len(authors),
#         'authors': [author.to_dict() for author in authors]  # List comprehension to convert all
#     })


# # GET /api/books/<id> - Get single book
# @app.route('/api/authors/<int:A_id>', methods=['GET'])
# def get_author(A_id):
#     author = Author.query.get(A_id)

#     if not author:
#         return jsonify({
#             'success': False,
#             'error': 'authors not found'
#         }), 404  # Return 404 status code

#     return jsonify({
#         'success': True,
#         'author': author.to_dict()
#     })


# # POST /api/books - Create new book
# @app.route('/api/authors', methods=['POST'])
# def create_author():
#     data = request.get_json()  # Get JSON data from request body

#     # Validation
#     if not data:
#         return jsonify({'success': False, 'error': 'No data provided'}), 400

#     if not data.get('name') or not data.get('city'):
#         return jsonify({'success': False, 'error': 'Name and City  are required'}), 400

#     # # Check for duplicate ISBN
#     # if data.get('isbn'):
#     #     existing = author.query.filter_by(isbn=data['isbn']).first()
#     #     if existing:
#     #         return jsonify({'success': False, 'error': 'ISBN already exists'}), 400

#     # Create book
#     new_author = Author(
#         name=data['name'],
#         city=data.get('city'),  # Optional field
#         bio=data.get('bio')
#     )

#     db.session.add(new_author)
#     db.session.commit()

#     return jsonify({
#         'success': True,
#         'message': 'Author created successfully',
#         'author': new_author.to_dict()
#     }), 201  # 201 = Created


# # PUT /api/books/<id> - Update author
# @app.route('/api/authors/<int:A_id>', methods=['PUT'])
# def update_author(A_id):
#     author = Author.query.get(A_id)

#     if not author:
#         return jsonify({'success': False, 'error': 'author not found'}), 404

#     data = request.get_json()

#     if not data:
#         return jsonify({'success': False, 'error': 'No data provided'}), 400

#     # Update fields if provided
#     # if 'A_id' in data:
#     #     author.A_id = data['A_id']
#     if 'name' in data:
#         author.name = data['name']
#     if 'city' in data:
#         author.city = data['city']
#     if 'bio' in data:
#         author.bio = data['bio']

#     db.session.commit()

#     return jsonify({
#         'success': True,
#         'message': 'Author updated successfully',
#         'author': author.to_dict()
#     })


# # DELETE /api/books/<id> - Delete book
# @app.route('/api/authors/<int:A_id>', methods=['DELETE'])
# def delete_author(A_id):
#     author = Author.query.get(A_id)

#     if not author:
#         return jsonify({'success': False, 'error': 'author not found'}), 404

#     db.session.delete(author)
#     db.session.commit()

#     return jsonify({
#         'success': True,
#         'message': 'author deleted successfully'
#     })


# # =============================================================================
# # BONUS: Search and Filter
# # =============================================================================

# # GET /api/books/search?q=python&author=john
# @app.route('/api/books/search', methods=['GET'])
# def search_books():
#     query = Book.query

#     # Filter by title (partial match)
#     title = request.args.get('q')  # Query parameter: ?q=python
#     if title:
#         query = query.filter(Book.title.ilike(f'%{title}%'))  # Case-insensitive LIKE

#     # Filter by author
#     author = request.args.get('author')
#     if author:
#         query = query.filter(Book.author.ilike(f'%{author}%'))

#     # Filter by year
#     year = request.args.get('year')
#     if year:
#         query = query.filter_by(year=int(year))

#     books = query.all()

#     return jsonify({
#         'success': True,
#         'count': len(books),
#         'books': [book.to_dict() for book in books]
#     })


# # =============================================================================
# # SIMPLE WEB PAGE FOR TESTING
# # =============================================================================

# @app.route('/')
# def index():
#     return '''
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Library CRUD Dashboard</title>
#     <style>
# /* ===== GLOBAL ===== */
# body {
#     font-family: 'Poppins', 'Segoe UI', sans-serif;
#     background: linear-gradient(135deg, #fdfcff, #eef2ff);
#     color: #1f2937;
#     padding: 30px;
# }

# /* ===== HEADINGS ===== */
# h1 {
#     font-size: 34px;
#     margin-bottom: 30px;
#     background: linear-gradient(90deg, #6366f1, #22c55e, #0ea5e9);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
# }

# h2 {
#     margin-bottom: 18px;
#     color: #4f46e5;
# }

# /* ===== SECTIONS ===== */
# .section {
#     background: #ffffff;
#     border-radius: 18px;
#     padding: 24px;
#     margin-bottom: 35px;
#     border-left: 6px solid #6366f1;
#     box-shadow: 0 14px 35px rgba(99, 102, 241, 0.18);
# }

# /* ===== BUTTONS (DEFAULT – VERY IMPORTANT) ===== */
# button {
#     background: linear-gradient(135deg, #6366f1, #8b5cf6); /* DEFAULT */
#     color: #ffffff;
#     border: none;
#     border-radius: 999px;
#     padding: 10px 18px;
#     font-size: 14px;
#     font-weight: 600;
#     cursor: pointer;
#     margin: 6px 6px 14px 0;
#     display: inline-block;
#     transition: all 0.25s ease;
# }

# button:hover {
#     transform: translateY(-2px);
#     box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
# }

# button:active {
#     transform: scale(0.95);
# }

# /* ===== BUTTON VARIANTS ===== */
# button.add {
#     background: linear-gradient(135deg, #22c55e, #4ade80);
# }

# button.edit {
#     background: linear-gradient(135deg, #f59e0b, #fbbf24);
#     color: #1f2937;
# }

# button.delete {
#     background: linear-gradient(135deg, #ef4444, #f87171);
# }

# /* ===== TABLE ===== */
# table {
#     width: 100%;
#     border-collapse: collapse;
#     margin-top: 14px;
#     background: #ffffff;
#     border-radius: 16px;
#     overflow: hidden;
#     box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
# }

# thead {
#     background: linear-gradient(90deg, #6366f1, #8b5cf6);
# }

# th {
#     padding: 14px;
#     font-size: 13px;
#     text-transform: uppercase;
#     letter-spacing: 0.06em;
#     color: #ffffff;
#     text-align: left;
# }

# td {
#     padding: 14px;
#     font-size: 15px;
#     border-bottom: 1px solid #e5e7eb;
# }

# tbody tr:hover {
#     background: #eef2ff;
# }

# /* ===== RESPONSIVE ===== */
# @media (max-width: 768px) {
#     h1 {
#         font-size: 26px;
#     }

#     button {
#         font-size: 13px;
#         padding: 8px 16px;
#     }
# }
# </style>

# </head>

# <body>

# <h1> BOOKS AND AUTHORS MANAGEMENT SYSTEM</h1>

# <!-- ================= BOOK SECTION ================= -->
# <div class="section">
#     <h2> Books</h2>

   
#     <button onclick="createBook()"> Add Book</button>

#     <table id="booksTable">
#         <thead>
#             <tr>
#                 <th>ID</th>
#                 <th>Title</th>
#                 <th>Author</th>
#                 <th>Year</th>
#                 <th>Actions</th>
#             </tr>
#         </thead>
#         <tbody></tbody>
#     </table>
# </div>

# <!-- ================= AUTHOR SECTION ================= -->
# <div class="section">
#     <h2>✍️ Authors</h2>


#     <button onclick="createAuthor()">Add Author</button>

#     <table id="authorsTable">
#         <thead>
#             <tr>
#                 <th>ID</th>
#                 <th>Name</th>
#                 <th>City</th>
#                 <th>Bio</th>
#                 <th>Actions</th>
#             </tr>
#         </thead>
#         <tbody></tbody>
#     </table>
# </div>

# <script>
# /* ================= BOOK FUNCTIONS ================= */

# function loadBooks() {
#     fetch('/api/books')
#         .then(res => res.json())
#         .then(data => {
#             const tbody = document.querySelector('#booksTable tbody');
#             tbody.innerHTML = '';
#             data.books.forEach(book => {
#                 tbody.innerHTML += `
#                 <tr>
#                     <td>${book.id}</td>
#                     <td>${book.title}</td>
#                     <td>${book.author}</td>
#                     <td>${book.year || ''}</td>
#                     <td>
#                         <button onclick="updateBook(${book.id})">✏️ Edit</button>
#                         <button onclick="deleteBook(${book.id})">🗑️ Delete</button>
#                     </td>
#                 </tr>`;
#             });
#         });
# }

# function createBook() {
#     const title = prompt("Enter book title:");
#     const author = prompt("Enter author:");
#     const year = prompt("Enter year:");

#     fetch('/api/books', {
#         method: 'POST',
#         headers: {'Content-Type': 'application/json'},
#         body: JSON.stringify({ title, author, year })
#     }).then(() => loadBooks());
# }


# function updateBook(id) {
#     const title = prompt("Enter new title:");
#     const author = prompt("Enter new author:");
#     const year = prompt("Enter new year:");
    

#     if (!title || !author) {
#         alert("Title and Author are required!");
#         return;
#     }

#     fetch(`/api/books/${id}`, {
#         method: 'PUT',
#         headers: { 'Content-Type': 'application/json' },
#         body: JSON.stringify({
#             title: title,
#             author: author,
#             year: year,
#             isbn: isbn
#         })
#     })
#     .then(res => res.json())
#     .then(data => {
#         alert("Book updated successfully ");
#         loadBooks();
#     });
# }



# function deleteBook(id) {
#     if (confirm("Delete this book?")) {
#         fetch(`/api/books/${id}`, { method: 'DELETE' })
#             .then(() => loadBooks());
#     }
# }

# /* ================= AUTHOR FUNCTIONS ================= */

# function loadAuthors() {
#     fetch('/api/authors')
#         .then(res => res.json())
#         .then(data => {
#             const tbody = document.querySelector('#authorsTable tbody');
#             tbody.innerHTML = '';
#             data.authors.forEach(author => {
#                 tbody.innerHTML += `
#                 <tr>
#                     <td>${author.A_id}</td>
#                     <td>${author.name}</td>
#                     <td>${author.city}</td>
#                     <td>${author.bio}</td>
#                     <td>
#                         <button onclick="updateAuthor(${author.A_id})">✏️ Edit</button>
#                         <button onclick="deleteAuthor(${author.A_id})">🗑️ Delete</button>
#                     </td>
#                 </tr>`;
#             });
#         });
# }

# function createAuthor() {
#     const name = prompt("Enter name:");
#     const city = prompt("Enter city:");
#     const bio = prompt("Enter bio:");

#     fetch('/api/authors', {
#         method: 'POST',
#         headers: {'Content-Type': 'application/json'},
#         body: JSON.stringify({ name, city, bio })
#     }).then(() => loadAuthors());
# }

# function updateAuthor(id) {
#     const city = prompt("Enter new city:");
#     const bio = prompt("Enter new bio:");

#     fetch(`/api/authors/${id}`, {
#         method: 'PUT',
#         headers: {'Content-Type': 'application/json'},
#         body: JSON.stringify({ city, bio })
#     }).then(() => loadAuthors());
# }

# function deleteAuthor(id) {
#     if (confirm("Delete this author?")) {
#         fetch(`/api/authors/${id}`, { method: 'DELETE' })
#             .then(() => loadAuthors());
#     }
# }

# /* Initial load */
# loadBooks();
# loadAuthors();
# </script>

# </body>

# </html>
# '''



# # =============================================================================
# # INITIALIZE DATABASE WITH SAMPLE DATA
# # =============================================================================

# def init_db():
#     with app.app_context():
#         db.create_all()

#         if Book.query.count() == 0:
#             sample_books = [
#                 Book(title='Python Crash Course', author='Eric Matthes', year=2019, isbn='978-1593279288'),
#                 Book(title='Flask Web Development', author='Miguel Grinberg', year=2018, isbn='978-1491991732'),
#                 Book(title='Clean Code', author='Robert C. Martin', year=2008, isbn='978-0132350884'),
#             ]
#             db.session.add_all(sample_books)
#             db.session.commit()
#             print('Sample books added!')


#         if Author.query.count() == 0:
#             sample_authors = [
#                 Author(name='Abc',city='nsk',bio='Bio 1'),
#                 Author(name='Author2',city='pune',bio='Bio 2'),
#                 Author(name='Author3',city='mumbai',bio='Bio 3'),
#             ]
#             db.session.add_all(sample_authors)
#             db.session.commit()
#             print('Sample author added!')


# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True)


# # =============================================================================
# # REST API CONCEPTS:
# # =============================================================================
# #
# # HTTP Method | CRUD      | Typical Use
# # ------------|-----------|---------------------------
# # GET         | Read      | Retrieve data
# # POST        | Create    | Create new resource
# # PUT         | Update    | Update entire resource
# # PATCH       | Update    | Update partial resource
# # DELETE      | Delete    | Remove resource
# #
# # =============================================================================
# # HTTP STATUS CODES:
# # =============================================================================
# #
# # Code | Meaning
# # -----|------------------
# # 200  | OK (Success)
# # 201  | Created
# # 400  | Bad Request (client error)
# # 404  | Not Found
# # 500  | Internal Server Error
# #
# # =============================================================================
# # KEY FUNCTIONS:
# # =============================================================================
# #
# # jsonify()           - Convert Python dict to JSON response
# # request.get_json()  - Get JSON data from request body
# # request.args.get()  - Get query parameters (?key=value)
# #
# # =============================================================================


# # =============================================================================
# # EXERCISE:
# # =============================================================================
# #
# # 1. Create new class say "Author" with fields id, name, bio, city with its table. 
# # Write all CRUD api routes for it similar to Book class.
# # Additionally try to link Book and Author class such that each book has one author and one author can have multiple books.

# # 1. Create 2 simple frontend using JavaScript fetch()
# # This is a bigger exercise. Create a frontend in HTML and JS that uses all api routes and displays data dynamically, along with create/edit/delete functionality.
# # Since the API is through n through accessible on the computer/server, you don't need to use render_template from flask, instead, 
# # you can directly use ipaddress:portnumber/apiroute from any where. So your HTML JS code can be anywhere on computer (not necessarily in flask)  

# # 3. Add pagination: `/api/books?page=1&per_page=10` 
# # Hint - the sqlalchemy provides paginate method. 
# # OPTIONAL - For ease of understanding, create a new api say /api/books-with-pagination which takes page number and number of books per page

# # 4. Add sorting: `/api/books?sort=title&order=desc`
# # OPTIONAL - For ease of understanding, create a new api say /api/books-with-sorting
# #
# # =============================================================================


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
    books = Book.query.all()
    result = []
    for b in books:
        result.append({
            "id": b.id,
            "title": b.title,
            "year": b.year,
            "author": {"id": b.author.id, "name": b.author.name} if b.author else None
        })
    return jsonify(result), 200

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
