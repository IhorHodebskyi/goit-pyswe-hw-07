from sqlalchemy import select
from models import Group, Teacher, Subject, Student, Grade
from database import get_async_session
import random
from faker import Faker

fake = Faker()

async def table_is_empty(session, table_class):
    result = await session.execute(select(table_class))
    return result.scalar() is None



async def insert_fake_data():

    async for session in get_async_session():
        
        if await table_is_empty(session, Group):
            group_names = ["Group A", "Group B", "Group C"]
            groups = [Group(name=name) for name in group_names]
            session.add_all(groups)
            await session.commit()

        if await table_is_empty(session, Teacher):
            teachers = [Teacher(name="John Doe")] + [Teacher(name=fake.name()) for _ in range(3)]
            session.add_all(teachers)
            await session.commit()

        if await table_is_empty(session, Subject):
            teacher_ids = [teacher.id for teacher in await session.execute(select(Teacher.id))]
            subjects = [
                Subject(name=name, teacher_id=random.choice(teacher_ids))
                for name in ["Math", "Physics", "Chemistry", "Biology", "History", "English", "IT"]
            ]
            session.add_all(subjects)
            await session.commit()

        if await table_is_empty(session, Student):
            group_ids = [group.id for group in await session.execute(select(Group.id))]
            students = [Student(name="Ihor", group_id=random.choice(group_ids))]
            students += [Student(name=fake.name(), group_id=random.choice(group_ids)) for _ in range(39)]
            session.add_all(students)
            await session.commit()


        if await table_is_empty(session, Grade):
            student_ids = [student.id for student in await session.execute(select(Student.id))]
            subject_ids = [subject.id for subject in await session.execute(select(Subject.id))]
            grades = [
                Grade(student_id=random.choice(student_ids), subject_id=random.choice(subject_ids),
                      grade=random.randint(50, 100), date=fake.date_this_decade())
                for _ in range(800)
            ]
            session.add_all(grades)
            await session.commit()

        print("Database successfully populated with fake data!")

	
