import asyncio
from seed import insert_fake_data
from orm import *


async def main():

    await insert_fake_data()

    top_stulent = await get_top_students(5)
    best_student = await get_best_student_by_subject("Math")
    avg_grade_by_group = await get_avg_grade_by_group("Math")
    avg_grade = await get_avg_grade()
    courses_by_teacher = await get_courses_by_teacher("John Doe")
    students_by_group = await get_students_by_group("Group A")
    grades_by_group_and_subject = await get_grades_by_group_and_subject("Group A", "Math")
    avg_grade_by_teacher = await get_avg_grade_by_teacher("John Doe")
    courses_by_student = await get_courses_by_student("Ihor")
    courses_by_student_and_teacher = await get_courses_by_student_and_teacher("Ihor", "John Doe")


    print("="*50)
    print("Top 5 Students:")
    print("-" * 50)
    print(f"{'Name':<30}{'Avg Grade':<10}")
    print("-" * 50)
    for student in top_stulent:
        print(student)        
    print("="*50)

    print("Best Student for 'Math':")
    print("-" * 50)
    print(f"{'Name':<30}{'Avg Grade':<10}")
    print("-" * 50)
    print(f"{best_student}")
    print("="*50)

    print("Average Grade by Group for 'Math':")
    print("-" * 50)
    print(f"{'Group':<30}{'Avg Grade':<10}")
    print("-" * 50)
    for group, avg_grade in avg_grade_by_group:
        print(f"{group:<30}{avg_grade:<10.2f}")
    print("="*50)

    print("Average Grade for the Entire Flow:")
    print("-" * 50)
    print(f"{'Avg Grade':<10}")
    print("-" * 50)
    print(f"{avg_grade:<10.2f}")
    print("="*50)

    print("Courses by Teacher:")
    print("-" * 50)
    print(f"{'Teacher':<30}{'Course':<30}")
    print("-" * 50)
    for teacher, course in courses_by_teacher:
        print(f"{teacher:<30}{course:<30}")
    print("="*50)

    print("Students by Group:")
    print("-" * 50)
    print(f"{'Group':<30}{'Student'}")
    print("-" * 50)
    for  student in students_by_group:
        print(f"{student[0]}")
    print("="*50)

    print("Grades by Group and Subject:")
    print("-" * 50)
    print(f"{'Group':<30}{'Subject':<30}")
    print("-" * 50)
    for group,  grade in grades_by_group_and_subject:
        print(f"{group:<30}{grade:<10}")
    print("="*50)

    print("Average Grade by Teacher:")
    print("-" * 50)
    print(f"{'Teacher':<30}{'Avg Grade':<10}")
    print("-" * 50)
    if len(avg_grade_by_teacher) > 0:
        for teacher in avg_grade_by_teacher:
            print(f"{teacher}")
    print("="*50)

    print("Courses by Student:")
    print("-" * 50)
    print(f"{'Student':<30}")
    print("-" * 50)
    for student in courses_by_student:
        print(f"{student[0]}")
    print("="*50)

    print("Courses by Student and Teacher:")
    print("-" * 50)
    print(f"{'Student':<30}{'Teacher':<30}{'Course':<30}")
    print("-" * 50)
    for student, teacher, course in courses_by_student_and_teacher:
        print(f"{student:<30}{teacher:<30}{course:<30}")
    print("="*50)

if __name__ == '__main__':
    asyncio.run(main())


