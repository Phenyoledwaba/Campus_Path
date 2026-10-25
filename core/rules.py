# core/rules.py

SA_SUBJECTS = [
    # Official Languages
    "Afrikaans Home Language", "Afrikaans First Additional Language",
    "English Home Language", "English First Additional Language",
    "isiNdebele Home Language", "isiNdebele First Additional Language",
    "isiXhosa Home Language", "isiXhosa First Additional Language",
    "isiZulu Home Language", "isiZulu First Additional Language",
    "Sepedi Home Language", "Sepedi First Additional Language",
    "Sesotho Home Language", "Sesotho First Additional Language",
    "Setswana Home Language", "Setswana First Additional Language",
    "siSwati Home Language", "siSwati First Additional Language",
    "Tshivenda Home Language", "Tshivenda First Additional Language",
    "Xitsonga Home Language", "Xitsonga First Additional Language",

    # Non-Official Languages (Second Additional Language)
    "French Second Additional Language",
    "German Second Additional Language",
    "Portuguese Second Additional Language",
    "Mandarin Second Additional Language",
    "Italian Second Additional Language",
    "Spanish Second Additional Language",
    "Latin Second Additional Language",
    "Arabic Second Additional Language",
    "Hebrew Second Additional Language",
    "South African Sign Language",

    # Core Subjects
    "Mathematics",
    "Mathematical Literacy",
    "Physical Sciences",
    "Life Sciences",
    "Accounting",
    "Business Studies",
    "Economics",
    "Geography",
    "History",
    "Information Technology",
    "Engineering Graphics and Design",
    "Agricultural Sciences",
    "Consumer Studies",
    "Hospitality Studies",
    "Tourism",
    "Religion Studies",
    "Visual Arts",
    "Music",
    "Life Orientation"
]


def calculate_aps(marks_dict):
    total_aps = 0
    count = 0
    for subject, percentage in marks_dict.items():
        # We usually exclude Life Orientation from the main APS calculation,
        # or it counts for fewer points. For simplicity, we'll count the best 6.
        if subject == "Life Orientation":
            continue

        if percentage >= 80:
            total_aps += 7
        elif percentage >= 70:
            total_aps += 6
        elif percentage >= 60:
            total_aps += 5
        elif percentage >= 50:
            total_aps += 4
        elif percentage >= 40:
            total_aps += 3
        elif percentage >= 30:
            total_aps += 2
        else:
            total_aps += 1

        count += 1
        if count == 6:  # Standard APS is calculated on the best 6 subjects
            break

    return total_aps


def filter_eligible_courses(student_aps, course_list):
    return [course for course in course_list if student_aps >= course.min_aps]
