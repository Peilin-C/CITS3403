# 📚 Study Buddy Finder

A web application for UWA students to find study partners, join study sessions, and connect with classmates in their units.

## Purpose

Study Buddy Finder helps UWA students connect with each other based on shared units, availability, and study preferences. Students can browse profiles, send buddy requests, join study sessions, and message their study buddies — all in one place.

## Features

- **User Authentication** — Sign up, log in and log out securely with hashed passwords
- **Student Profiles** — Set up your profile with degree, units, availability, study style and preferences
- **Browse Users** — Find other students with live search and filter by unit, availability and study style
- **Buddy Requests** — Send, accept and decline buddy requests with notification badges
- **Study Sessions** — Create, join, leave and edit study sessions with participant tracking
- **Messaging** — Chat with accepted study buddies with real-time character counter
- **Notifications** — Bell icon with badge showing pending buddy requests
- **Security** — CSRF protection on all forms, passwords stored as salted hashes

## Team Members

| UWA ID | Name | GitHub Username |
|--------|------|----------------|
| 24253549 | Bhavya Narula | Bhavya-narula |
| 23997337 | Fatima Sher | fatimasher0 |
| 24389729 | Peilin Cai | Peilin-C |
| 25017991 | Saffron Coupland | SAFFRONCode24 |

## How to Launch

### Prerequisites
- Python 3.10+
- pip

### Steps

1. Clone the repository:

git clone https://github.com/Peilin-C/CITS3403.git
cd CITS3403

2. Install dependencies:

pip install -r requirements.txt

3. Run the application:

python run.py

4. Open your browser and go to:

http://127.0.0.1:5000

## How to Run Tests

### Unit Tests

python -m pytest tests.py -v

### Selenium Tests

Make sure the Flask app is running first (python run.py), then in a separate terminal:

python -m pytest tests/ -v

## Database

The application uses SQLite with SQLAlchemy. The database is created automatically when you first run the app. No setup required.

**Schema:**
- `User` — student profiles with authentication
- `StudySession` — study sessions with location, time and capacity
- `session_participants` — junction table tracking session attendance
- `BuddyRequest` — friend requests with pending/accepted/declined status
- `Message` — messages between accepted buddies with read/unread tracking

## Technologies Used

- **Backend** — Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend** — HTML, CSS, JavaScript, Bootstrap 5.3.3
- **Database** — SQLite
- **Testing** — pytest, Selenium
