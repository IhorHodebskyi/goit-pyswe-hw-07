
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