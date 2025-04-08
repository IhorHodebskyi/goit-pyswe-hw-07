import asyncio
from seed import insert_fake_data
from models import Group, Teacher, Subject, Student, Grade
from sqlalchemy import select, func
from database import get_async_session

async def get_top_students(limit: int):
    async for session in get_async_session():
        result = await session.execute(
            select(Student, func.avg(Grade.grade).label('avg_grade'))
            .join(Grade, Student.id == Grade.student_id)
            .group_by(Student.id)
            .order_by(func.avg(Grade.grade).desc())
            .limit(limit)
        )
        students = result.all()
        return [f"Student: {student.name}, Avg Grade: {avg_grade}" for student, avg_grade in students]


async def get_best_student_by_subject(subject_name: int):
    async for session in get_async_session():
        result = await session.execute(
            select(Student, func.avg(Grade.grade).label("avg_grade"))
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Subject.name == subject_name)
            .group_by(Student.id)
            .order_by(func.avg(Grade.grade).desc())
            .limit(1)
        )
        best_student = result.first()
        if best_student:
            student, avg_grade = best_student
            return f"Best student: {student.name}, Avg Grade: {avg_grade}"
        else:
            return "No students found for this subject."

async def get_avg_grade_by_group(subject_name: str):
    async for session in get_async_session():
        result = await session.execute(
            select(Group.name, func.avg(Grade.grade).label('avg_grade'))
            .join(Student, Group.id == Student.group_id)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Subject.name == subject_name)
            .group_by(Group.id)
        )
        return result.fetchall()

async def get_avg_grade():
    async for session in get_async_session():
        result = await session.execute(
            select(func.avg(Grade.grade).label('avg_grade'))
        )
        return result.scalar()

async def get_courses_by_teacher(teacher_name: str):
    async for session in get_async_session():
        result = await session.execute(
            select(Subject.name)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .filter(Teacher.name == teacher_name)
        )
        return result.fetchall()

async def get_students_by_group(group_name: str):
    async for session in get_async_session():
        result = await session.execute(
            select(Student.name)
            .join(Group, Student.group_id == Group.id)
            .filter(Group.name == group_name)
        )
        return result.fetchall()

async def get_grades_by_group_and_subject(group_name: str, subject_name: str):
    async for session in get_async_session():
        result = await session.execute(
            select(Student.name, Grade.grade)
            .join(Group, Student.group_id == Group.id)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Group.name == group_name)
            .filter(Subject.name == subject_name)
        )
        return result.fetchall()

async def get_avg_grade_by_teacher(teacher_name: str):
    async for session in get_async_session():
        result = await session.execute(
            select(func.avg(Grade.grade).label('avg_grade'))
            .join(Subject, Grade.subject_id == Subject.id)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .filter(Teacher.name == teacher_name)
        )
        return result.all() 

async def get_courses_by_student(student_name: str):
    async for session in get_async_session():
        result = await session.execute(
            select(Subject.name)
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Grade.student_id == Student.id)
            .filter(Student.name == student_name)
        )
        return result.fetchall()

async def get_courses_by_student_and_teacher(student_name: str, teacher_name: str):
    async for session in get_async_session():
        result = await session.execute(
            select(Subject.name)
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Grade.student_id == Student.id)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .filter(Student.name == student_name)
            .filter(Teacher.name == teacher_name)
        )
        return result.fetchall()

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
    print(f"{'Group':<30}{'Subject':<30}{'Grade':<10}")
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
    print(f"{'Student':<30}{'Course':<30}")
    print("-" * 50)
    for student in courses_by_student:
        print(f"{student}")
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


