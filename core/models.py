class Course:
    def __init__(self, id, institution, course_name, min_aps, faculty):
        self.id = id
        self.institution = institution
        self.course_name = course_name
        self.min_aps = min_aps
        self.faculty = faculty

class Student:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.marks = {}
        self.aps = 0