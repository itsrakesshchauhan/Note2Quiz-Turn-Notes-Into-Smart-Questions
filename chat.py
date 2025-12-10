from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import google.generativeai as genai
import os
import json

# Configure Gemini API
genai.configure(api_key="AIzaSyC7WUCv_Um6uOHjGSWEMD3-M6mZQ_KllVI")  # Replace with your actual API key

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'courses'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

def load_users():
    try:
        with open('data/users.json', 'r') as file:
            users_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        users_data = []
    return {user['id']: User(user['id'], user['username'], user['password'], user['role']) for user in users_data}

def save_users(users):
    with open('data/users.json', 'w') as file:
        json.dump([{'id': user.id, 'username': user.username, 'password': user.password, 'role': user.role} for user in users.values()], file)

def load_courses():
    try:
        with open('data/courses.json', 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_courses(courses):
    with open('data/courses.json', 'w') as file:
        json.dump(courses, file)

users = load_users()
courses = load_courses()

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', courses=courses)

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        prompt = f"Generate 5 exam-style questions based on the following text:\n\n{text}"
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        questions = response.text.strip()
        return jsonify({'questions': questions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = next((user for user in users.values() if user.username == username), None)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check username and password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(id=len(users) + 1, username=username, password=hashed_password, role=role)
        users[new_user.id] = new_user
        save_users(users)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'teacher':
        user_courses = [course for course in courses if course['teacher_id'] == current_user.id]
    else:
        user_courses = courses
    return render_template('dashboard.html', courses=user_courses)

@app.route('/upload_course', methods=['GET', 'POST'])
@login_required
def upload_course():
    if current_user.role != 'teacher':
        flash('You do not have permission to upload courses.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        video = request.files.get('video')

        if video:
            filename = secure_filename(video.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(video_path)

            new_course = {
                'id': len(courses) + 1,
                'title': title,
                'description': description,
                'video_path': video_path,
                'teacher_id': current_user.id
            }

            courses.append(new_course)
            save_courses(courses)
            flash('Course uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('upload_course.html')

@app.route('/courses/<int:course_id>/video')
@login_required
def get_video(course_id):
    course = next((c for c in courses if c['id'] == course_id), None)
    if course:
        return send_from_directory(os.path.dirname(course['video_path']), os.path.basename(course['video_path']))
    else:
        return 'Video not found', 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
