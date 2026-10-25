import sqlite3
from core.models import Course

DB_NAME = "campuspath.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)""")
        
    cur.execute("""CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY, institution TEXT, course_name TEXT, 
        min_aps INTEGER, faculty TEXT)""")
    
    # Seed demo user
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("student", "demo123"))
        
    # Seed REAL courses (UJ, Wits, TUT)
    cur.execute("SELECT COUNT(*) FROM courses")
    if cur.fetchone()[0] == 0:
        courses = [
            # --- UJ (University of Johannesburg) ---
            ("University of Johannesburg", "Diploma in Business IT", 24, "ICT"),
            ("University of Johannesburg", "Diploma in Sport Management", 26, "Humanities"),
            ("University of Johannesburg", "BCom Accounting", 34, "Commerce"),
            ("University of Johannesburg", "BSc Computer Science", 38, "Science"),
            ("University of Johannesburg", "BEng Tech in Civil Engineering", 40, "Engineering"),
            
            # --- Wits University ---
            ("Wits University", "BA in Performing Arts", 28, "Humanities"),
            ("Wits University", "BCom Finance", 38, "Commerce"),
            ("Wits University", "BA Law", 36, "Humanities"),
            ("Wits University", "BSc Engineering", 42, "Engineering"),
            ("Wits University", "BSc in Biological Sciences", 34, "Science"),
            
            # --- TUT (Tshwane University of Technology) ---
            ("Tshwane University of Technology", "Diploma in Accounting", 24, "Commerce"),
            ("Tshwane University of Technology", "Diploma in IT", 26, "ICT"),
            ("Tshwane University of Technology", "Diploma in Hospitality Management", 28, "Tourism"),
            ("Tshwane University of Technology", "BEng Tech in Electrical Engineering", 32, "Engineering"),
            ("Tshwane University of Technology", "BSc in Agriculture", 30, "Science")
        ]
        for inst, course, aps, faculty in courses:
            cur.execute("INSERT INTO courses (institution, course_name, min_aps, faculty) VALUES (?, ?, ?, ?)", (inst, course, aps, faculty))

    conn.commit()
    conn.close()

def check_login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user is not None

def get_all_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, institution, course_name, min_aps, faculty FROM courses")
    rows = cur.fetchall()
    conn.close()
    return [Course(row[0], row[1], row[2], row[3], row[4]) for row in rows]