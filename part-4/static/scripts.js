// document.addEventListener('DOMContentLoaded', () => {
//     fetchAuthors();
//     fetchBooks();

//     // Author form
//     const authorForm = document.getElementById('add-author-form');
//     authorForm.addEventListener('submit', addAuthor);

//     // Book form
//     const bookForm = document.getElementById('add-book-form');
//     bookForm.addEventListener('submit', addBook);
// });

// // ---------- AUTHORS ----------
// function fetchAuthors() {
//     fetch('http://127.0.0.1:5000/api/authors')
//         .then(response => {
//             if (!response.ok) throw new Error('Failed to fetch authors');
//             return response.json();
//         })
//         .then(data => renderAuthors(data))
//         .catch(error => console.error(error));
// }

// function renderAuthors(authors) {
//     const list = document.getElementById('authors-list');
//     list.innerHTML = '';

//     authors.forEach(author => {
//         const li = document.createElement('li');
//         li.textContent = `${author.name} - ${author.email}`;
//         list.appendChild(li);
//     });

//     // Optionally populate author dropdown for book form
//     const authorSelect = document.getElementById('book-author-id');
//     if (authorSelect) {
//         authorSelect.innerHTML = '';
//         authors.forEach(author => {
//             const option = document.createElement('option');
//             option.value = author.id;
//             option.textContent = author.name;
//             authorSelect.appendChild(option);
//         });
//     }
// }

// function addAuthor(event) {
//     event.preventDefault();
//     const name = document.getElementById('author-name').value;
//     const email = document.getElementById('author-email').value;

//     const data = { name, email };
//     console.log('Sending Author data:', data);

//     fetch('http://127.0.0.1:5000/api/authors', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(data)
//     })
//     .then(response => {
//         if (!response.ok) throw new Error('Failed to add author');
//         return response.json();
//     })
//     .then(data => {
//         console.log('Author added:', data);
//         fetchAuthors();
//         document.getElementById('add-author-form').reset();
//     })
//     .catch(error => console.error(error));
// }

// // ---------- BOOKS ----------
// function fetchBooks() {
//     fetch('http://127.0.0.1:5000/api/books')
//         .then(response => {
//             if (!response.ok) throw new Error('Failed to fetch books');
//             return response.json();
//         })
//         .then(data => renderBooks(data))
//         .catch(error => console.error(error));
// }

// function renderBooks(books) {
//     const list = document.getElementById('books-list');
//     list.innerHTML = '';

//     books.forEach(book => {
//         const li = document.createElement('li');
//         li.textContent = `${book.title} (${book.year || 'N/A'}) - Author: ${book.author.name}`;
//         list.appendChild(li);
//     });
// }

// function addBook(event) {
//     event.preventDefault();
//     const title = document.getElementById('book-title').value;
//     const year = parseInt(document.getElementById('book-year').value) || null;
//     const author_id = parseInt(document.getElementById('book-author-id').value);

//     const data = { title, year, author_id };
//     console.log('Sending Book data:', data);

//     fetch('http://127.0.0.1:5000/api/books', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(data)
//     })
//     .then(response => {
//         if (!response.ok) throw new Error('Failed to add book');
//         return response.json();
//     })
//     .then(data => {
//         console.log('Book added:', data);
//         fetchBooks();
//         document.getElementById('add-book-form').reset();
//     })
//     .catch(error => console.error(error));
// }

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('authorsBody')) initAuthorsPage();
    if (document.getElementById('booksBody')) initBooksPage();
});

const API_AUTHORS = "http://127.0.0.1:5000/api/authors";
const API_BOOKS = "http://127.0.0.1:5000/api/books";

let authorsCache = [];
let editingAuthorId = null;
let editingBookId = null;

// -------------------- AUTHORS --------------------
function initAuthorsPage() {
    loadAuthors();

    const addBtn = document.getElementById("add-author-btn");
    const formContainer = document.getElementById("authorFormContainer");
    const submitBtn = document.getElementById("authorFormSubmit");
    const cancelBtn = document.getElementById("authorFormCancel");

    addBtn.addEventListener("click", () => {
        editingAuthorId = null;
        document.getElementById("authorFormTitle").innerText = "Add Author";
        document.getElementById("authorName").value = "";
        document.getElementById("authorEmail").value = "";
        formContainer.style.display = "block";
    });

    cancelBtn.addEventListener("click", () => formContainer.style.display = "none");

    submitBtn.addEventListener("click", () => {
        const name = document.getElementById("authorName").value.trim();
        const email = document.getElementById("authorEmail").value.trim();
        if (!name || !email) return alert("All fields are required");

        const payload = { name, email };
        let url = API_AUTHORS;
        let method = "POST";

        if (editingAuthorId) {
            url += `/${editingAuthorId}`;
            method = "PUT";
        }

        fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        }).then(() => {
            formContainer.style.display = "none";
            loadAuthors();
        });
    });
}

function loadAuthors() {
    fetch(API_AUTHORS)
        .then(res => res.json())
        .then(data => {
            authorsCache = data;
            const tbody = document.getElementById("authorsBody");
            tbody.innerHTML = "";
            data.forEach(a => {
                tbody.innerHTML += `
                <tr>
                    <td>${a.id}</td>
                    <td>${a.name}</td>
                    <td>${a.email}</td>
                    <td>${a.books ? a.books.length : 0}</td>
                    <td>
                        <button class="edit" onclick="editAuthor(${a.id})">Edit</button>
                        <button class="delete" onclick="deleteAuthor(${a.id})">Delete</button>
                    </td>
                </tr>`;
            });
        });
}

window.editAuthor = function(id) {
    const author = authorsCache.find(a => a.id === id);
    if (!author) return;

    editingAuthorId = id;
    document.getElementById("authorFormTitle").innerText = "Edit Author";
    document.getElementById("authorName").value = author.name;
    document.getElementById("authorEmail").value = author.email;
    document.getElementById("authorFormContainer").style.display = "block";
}

window.deleteAuthor = function(id) {
    if (confirm("Delete author?")) {
        fetch(`${API_AUTHORS}/${id}`, { method: "DELETE" })
            .then(loadAuthors);
    }
}

// -------------------- BOOKS --------------------
function initBooksPage() {
    loadBooks();

    const addBtn = document.getElementById("add-book-btn");
    const formContainer = document.getElementById("bookFormContainer");
    const submitBtn = document.getElementById("bookFormSubmit");
    const cancelBtn = document.getElementById("bookFormCancel");

    addBtn.addEventListener("click", async () => {
        editingBookId = null;
        document.getElementById("bookFormTitle").innerText = "Add Book";
        document.getElementById("bookTitle").value = "";
        document.getElementById("bookYear").value = "";
        await fillAuthorsSelect();
        formContainer.style.display = "block";
    });

    cancelBtn.addEventListener("click", () => formContainer.style.display = "none");

    submitBtn.addEventListener("click", async () => {
        const title = document.getElementById("bookTitle").value.trim();
        const year = parseInt(document.getElementById("bookYear").value) || null;
        const authorId = parseInt(document.getElementById("bookAuthor").value);

        if (!title || !authorId) return alert("Title and Author are required");

        const payload = { title, year, author_id: authorId };
        let url = API_BOOKS;
        let method = "POST";

        if (editingBookId) {
            url += `/${editingBookId}`;
            method = "PUT";
        }

        fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        }).then(() => {
            formContainer.style.display = "none";
            loadBooks();
        });
    });
}

async function fillAuthorsSelect() {
    if (authorsCache.length === 0) {
        await fetch(API_AUTHORS)
            .then(res => res.json())
            .then(data => authorsCache = data);
    }
    const select = document.getElementById("bookAuthor");
    select.innerHTML = "";
    authorsCache.forEach(a => {
        const option = document.createElement("option");
        option.value = a.id;
        option.textContent = a.name;
        select.appendChild(option);
    });
}

function loadBooks() {
    fetch(API_BOOKS)
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById("booksBody");
            tbody.innerHTML = "";
            data.forEach(b => {
                tbody.innerHTML += `
                <tr>
                    <td>${b.id}</td>
                    <td>${b.title}</td>
                    <td>${b.author ? b.author.name : "N/A"}</td>
                    <td>${b.year || ""}</td>
                    <td>
                        <button class="edit" onclick="editBook(${b.id})">Edit</button>
                        <button class="delete" onclick="deleteBook(${b.id})">Delete</button>
                    </td>
                </tr>`;
            });
        });
}

window.editBook = async function(id) {
    await fillAuthorsSelect();
    const book = await fetch(`${API_BOOKS}/${id}`).then(res => res.json());
    if (!book) return;

    editingBookId = id;
    document.getElementById("bookFormTitle").innerText = "Edit Book";
    document.getElementById("bookTitle").value = book.title;
    document.getElementById("bookYear").value = book.year || "";
    document.getElementById("bookAuthor").value = book.author ? book.author.id : "";
    document.getElementById("bookFormContainer").style.display = "block";
}

window.deleteBook = function(id) {
    if (confirm("Delete book?")) {
        fetch(`${API_BOOKS}/${id}`, { method: "DELETE" })
            .then(loadBooks);
    }
}
