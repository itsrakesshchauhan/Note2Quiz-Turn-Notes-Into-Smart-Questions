# Note2Quiz – Turn Notes Into Smart Questions ✨

Note2Quiz is an AI-powered learning platform for **college students and teachers**.  
Upload lecture notes, PDFs, or study material and instantly generate **exam-style questions and quizzes** to make preparation faster and more effective.

> 🚀 Built using **Flask**, **Google Gemini** and a simple JSON-based data layer (no database setup required).

---

## 🧠 What Problem Does It Solve?

- Students struggle to **figure out important questions** from long notes.
- Teachers spend a lot of time **manually creating quizzes, question papers, and assignments**.
- There is no simple platform where:
  - Teachers can upload and share course content.
  - Students can **practice auto-generated, syllabus-based questions** anytime.

**Note2Quiz** bridges this gap by turning raw notes into structured practice material.

---

## 💡 Core Features

### 👨‍🎓 For Students

- Upload notes (**PDF / text**).
- Auto-generate:
  - ✅ Multiple Choice Questions (MCQs)  
  - ✅ Short answer questions  
  - ✅ Long answer / theory questions  
- Practice in **quiz mode** (with timer support in UI logic).
- Generate **unlimited question sets** from the same notes.
- Use teacher-uploaded course materials for self-study.

---

### 👩‍🏫 For Teachers

- Register as **Teacher** and log in to a dedicated dashboard.
- Create and manage **courses**.
- Upload lecture videos / materials (stored under `courses/`).
- AI-powered generation of:
  - ✅ Quizzes  
  - ✅ Assignments  
  - ✅ Question papers  
- Share content with all registered students (same platform).

---

## 🏗️ Tech Stack

- **Backend:** Flask, Flask-Login
- **AI Model:** Google Generative AI (Gemini – `gemini-1.5-flash`)
- **Auth & Security:**  
  - `flask_login` for login/session management  
  - `werkzeug.security` for password hashing
- **Storage:**
  - JSON files in `data/` (`users.json`, `courses.json`)
  - Uploaded course videos in `courses/`
- **Frontend:** HTML templates (Jinja2) + JavaScript

---

## 📁 Project Structure

```bash
Note2Quiz-Turn-Notes-Into-Smart-Questions/
├── chat.py               # Main Flask application
├── data/
│   ├── users.json        # User credentials & roles (JSON)
│   └── courses.json      # Course metadata (JSON)
├── templates/            # HTML templates (index, login, dashboard, etc.)
├── js/                   # Frontend JavaScript files
├── courses/              # Uploaded course videos (created at runtime)
├── LICENSE               # MIT License
└── README.md             # Project documentation
