# core/rules.py

SA_SUBJECTS = [
    "Accounting", "Agricultural Sciences", "Business Studies", "Consumer Studies", 
    "Economics", "Engineering Graphics and Design", "Geography", "History", 
    "Hospitality Studies", "Information Technology", "Life Sciences", 
    "Life Orientation", "Mathematical Literacy", "Mathematics", 
    "Music", "Physical Sciences", "Religion Studies", "Tourism", "Visual Arts"
]

def calculate_aps(marks_dict):
    total_aps = 0
    count = 0
    for subject, percentage in marks_dict.items():
        # We usually exclude Life Orientation from the main APS calculation, 
        # or it counts for fewer points. For simplicity, we'll count the best 6.
        if subject == "Life Orientation":
            continue
            
        if percentage >= 80: total_aps += 7
        elif percentage >= 70: total_aps += 6
        elif percentage >= 60: total_aps += 5
        elif percentage >= 50: total_aps += 4
        elif percentage >= 40: total_aps += 3
        elif percentage >= 30: total_aps += 2
        else: total_aps += 1
        
        count += 1
        if count == 6: # Standard APS is calculated on the best 6 subjects
            break
            
    return total_aps

def filter_eligible_courses(student_aps, course_list):
    return [course for course in course_list if student_aps >= course.min_aps]