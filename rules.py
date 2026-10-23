def calculate_aps(marks_dict):
    total_aps = 0
    for subject, percentage in marks_dict.items():
        if percentage >= 80: total_aps += 7
        elif percentage >= 70: total_aps += 6
        elif percentage >= 60: total_aps += 5
        elif percentage >= 50: total_aps += 4
        elif percentage >= 40: total_aps += 3
        elif percentage >= 30: total_aps += 2
        else: total_aps += 1
    return total_aps

def filter_eligible_courses(student_aps, course_list):
    return [course for course in course_list if student_aps >= course.min_aps]
