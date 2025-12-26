# Small Quiz App

A simple **Quiz Application** built using **Django (Backend)** and **HTML + Tailwind CSS (Frontend)**.  

This app allows users to attempt quizzes, submit answers, view scores, and track quiz history.  
It also includes an **Admin Dashboard** to manage quizzes, questions, and events.



---

## Features

### User Features
- Register and login as a user
- Attempt quizzes and submit answers
- View scores after quiz submission
- Track quiz history
- Responsive UI using **Tailwind CSS**
---

### Admin Features
- Login as an admin
- Add, delete quizzes
- Add, delete quiz questions
- Add, delete events
- View all quiz submissions and user history

### Admin Credentials
- **Username:** `quiz_admin`
- **Password:** `quiz123`


### Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** HTML, Tailwind CSS, JavaScript ( use AI for frontend )
- **Database:** SQLite (Default)


---

##  Setup Instructions

### 1 Download Project

- Open the GitHub repository  
- Click **Code → Download ZIP**  
- Extract the ZIP file  
- Open the extracted folder in terminal / command prompt  

---

### 2️ Create Virtual Environment and Setup

```bash
# Create Virtual Environment
python -m venv venv

# Activate Environment

## Windows
venv\Scripts\activate

## Linux / macOS
source venv/bin/activate

# Install Dependencies
pip install django


# Apply Database Migrations
python manage.py makemigrations
python manage.py migrate

# Create Superuser (Optional)
python manage.py createsuperuser

# Run Development Server
python manage.py runserver

# Open in Browser
# http://127.0.0.1:8000/
