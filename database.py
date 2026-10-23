import sqlite3
from models import Course

DB_NAME = "campuspath.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY, institution TEXT, course_name TEXT, 
        min_aps INTEGER, faculty TEXT)""")
    conn.commit()
    conn.close()

def get_all_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, institution, course_name, min_aps, faculty FROM courses")
    rows = cur.fetchall()
    conn.close()
    return [Course(row[0], row[1], row[2], row[3], row[4]) for row in rows]