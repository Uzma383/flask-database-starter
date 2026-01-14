# """
# Part 3: Flask-SQLAlchemy ORM
# ============================
# Say goodbye to raw SQL! Use Python classes to work with databases.

# What You'll Learn:
# - Setting up Flask-SQLAlchemy
# - Creating Models (Python classes = database tables)
# - ORM queries instead of raw SQL
# - Relationships between tables (One-to-Many)

# Prerequisites: Complete part-1 and part-2
# Install: pip install flask-sqlalchemy
# """



"""
Part 3: Flask-SQLAlchemy ORM
============================
Say goodbye to raw SQL! Use Python classes to work with databases.

What You'll Learn:
- Setting up Flask-SQLAlchemy
- Creating Models (Python classes = database tables)
- ORM queries instead of raw SQL
- Relationships between tables (One-to-Many)

Prerequisites: Complete part-1 and part-2
Install: pip install flask-sqlalchemy
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =============================================================================
# MODELS (Python Classes = Database Tables)
# =============================================================================

# class Teacher(db.Model):   # NEW MODEL
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     # One Teacher teaches Many Courses
#     courses = db.relationship('Course', backref='teacher', lazy=True)

#     def __repr__(self):
#         return f'<Teacher {self.name}>'

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # One Teacher teaches ONE Course
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), unique=True)
    course = db.relationship('Course', backref='teacher', uselist=False)
    

    def __repr__(self):
        return f'<Teacher {self.name}>'

    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Course {self.name}>'



# class Course(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)

#     # Foreign Key: Each course has one teacher
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

#     # One Course has Many Students
#     students = db.relationship('Student', backref='course', lazy=True)

#     def __repr__(self):
#         return f'<Course {self.name}>'


# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     # Foreign Key: Links student to a course
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

#     def __repr__(self):
#         return f'<Student {self.name}>'
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Student belongs to one course
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='students')

    def __repr__(self):
        return f'<Student {self.name}>'


# =============================================================================
# ROUTES
# =============================================================================

# @app.route('/')
# def index():
#     students = Student.query.all()   # ORDER BY example  
#     return render_template('index.html', students=students)
@app.route('/')
def index():
    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template('index.html', students=students, teachers=teachers)



@app.route('/courses')
def courses():
    all_courses = Course.query.order_by(Course.name).all()
    return render_template('courses.html', courses=all_courses)


@app.route('/teachers')
def teachers():
    all_teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=all_teachers)


@app.route('/top-students')
def top_students():
    """Example: LIMIT query"""
    students = Student.query.limit(3).all()
    return render_template('index.html', students=students)


@app.route('/search')
def search_students():
    """Example: FILTER query"""
    keyword = request.args.get('q', '')
    students = Student.query.filter(Student.name.like(f"%{keyword}%")).all()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course_id = request.form['course_id']

        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            flash("Email already exists! Please use a different email.", "danger")
            return redirect(url_for('add_student'))

        new_student = Student(name=name, email=email, course_id=course_id)
        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('add.html', courses=courses)


@app.route('/edit-student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course_id = request.form['course_id']
        db.session.commit()
        flash('Student updated!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('edit_students.html', student=student, courses=courses)



@app.route('/delete-student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted!', 'danger')
    return redirect(url_for('index'))



@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        print("----- I M Inside Post -----")
        name = request.form['name']
        description = request.form.get('description', '')
        teacher_id = request.form['teacher_id']

        new_course = Course(name=name, description=description, teacher_id=teacher_id)
        db.session.add(new_course)
        db.session.commit()

        flash('Course added!', 'success')
        return redirect(url_for('courses'))

    teachers = Teacher.query.all()
    return render_template('add_course.html', teachers=teachers)


# @app.route('/add_teacher', methods=['GET', 'POST'])
# def add_teacher():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']

#         new_teacher = Teacher(name=name, email=email)
#         db.session.add(new_teacher)
#         db.session.commit()

#         flash('Teacher added!', 'success')
#         return redirect(url_for('teachers'))

#     return render_template('add_teacher.html')


@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course_id = request.form['course_id']

        existing_teacher = Teacher.query.filter_by(email=email).first()
        if existing_teacher:
            flash("Email already exists! Please use a different email.", "danger")
            return redirect(url_for('add_teacher'))

        # Check if course is already assigned to another teacher
        assigned = Teacher.query.filter_by(course_id=course_id).first()
        if assigned:
            flash("This course is already assigned to another teacher!", "danger")
            return redirect(url_for('add_teacher'))

        new_teacher = Teacher(name=name, email=email, course_id=course_id)
        db.session.add(new_teacher)
        db.session.commit()

        flash('Teacher added successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('add_teacher.html', courses=courses)



@app.route('/edit-teacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)

    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.email = request.form['email']
        db.session.commit()
        flash('Teacher updated!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_teachers.html', teacher=teacher)



@app.route('/delete-teacher/<int:id>')
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher deleted!', 'danger')
    return redirect(url_for('index'))


# =============================================================================
# CREATE TABLES AND ADD SAMPLE DATA
# =============================================================================

def init_db():
    with app.app_context():
        db.create_all()

        # Add sample teachers
        if Teacher.query.count() == 0:
            teachers = [
                Teacher(name='Mr. Sharma', email='sharma@gmail.com'),
                Teacher(name='Ms. Khan', email='khan@gmail.com'),
            ]
            db.session.add_all(teachers)
            db.session.commit()

        # Add sample courses
        if Course.query.count() == 0:
            courses = [
                Course(name='Python Basics', description='Learn Python fundamentals'),
                Course(name='Web Development', description='HTML, CSS, Flask'),
                Course(name='Data Science', description='Data analysis with Python'),
            ]
            db.session.add_all(courses)
            db.session.commit()
            print('Sample teachers and courses added!')


# =============================================================================

if __name__ == '__main__':
    init_db()
    app.run(debug=True)





# # =============================================================================
# # ORM vs RAW SQL COMPARISON:
# # =============================================================================
# #
# # Operation      | Raw SQL                          | SQLAlchemy ORM
# # ---------------|----------------------------------|---------------------------
# # Get all        | SELECT * FROM students           | Student.query.all()
# # Get by ID      | SELECT * WHERE id = ?            | Student.query.get(id)
# # Filter         | SELECT * WHERE name = ?          | Student.query.filter_by(name='John')
# # Insert         | INSERT INTO students VALUES...   | db.session.add(student)
# # Update         | UPDATE students SET...           | student.name = 'New'; db.session.commit()
# # Delete         | DELETE FROM students WHERE...    | db.session.delete(student)
# #
# # =============================================================================
# # COMMON QUERY METHODS:
# # =============================================================================
# #
# # Student.query.all()                    - Get all records
# # Student.query.first()                  - Get first record
# # Student.query.get(1)                   - Get by primary key
# # Student.query.get_or_404(1)            - Get or show 404 error
# # Student.query.filter_by(name='John')   - Filter by exact value
# # Student.query.filter(Student.name.like('%john%'))  - Filter with LIKE
# # Student.query.order_by(Student.name)   - Order results
# # Student.query.count()                  - Count records
# #
# # =============================================================================


# # =============================================================================
# # EXERCISE:
# # =============================================================================
# #
# # 1. Add a `Teacher` model with a relationship to Course
# # 2. Try different query methods: `filter()`, `order_by()`, `limit()`
# #
# # =============================================================================
