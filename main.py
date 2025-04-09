import asyncio
import argparse
from datetime import datetime
from seed import insert_fake_data
from orm import *
from crud import *
from database import get_async_session


MODEL_MAP = {
    "Group": Group,
    "Teacher": Teacher,
    "Subject": Subject,
    "Student": Student,
    "Grade": Grade,
}

async def main():
    parser = argparse.ArgumentParser(description="CCLI for robots with database")
    parser.add_argument("-a", "--action", required=True, choices=["create", "list", "update", "remove"], help="CRUD operation")
    parser.add_argument("-m", "--model", required=True, choices=MODEL_MAP.keys(), help="Operation model")
    
    parser.add_argument("--id", type=int, help="ID for renovation or renovation")
    parser.add_argument("-n", "--name", help="Name (Teacher, Group, Subject, Student)")
    parser.add_argument("--group_id", type=int, help="ID групи (Student)")
    parser.add_argument("--teacher_id", type=int, help="ID ticher (Subject)")
    parser.add_argument("--subject_id", type=int, help="ID item (Grade)")
    parser.add_argument("--student_id", type=int, help="ID student (Grade)")
    parser.add_argument("--grade", type=int, help="grade (Grade)")
    parser.add_argument("--date", help="Date in format YYYY-MM-DD (Grade)")

    args = parser.parse_args()

    async for session in get_async_session():
        model = MODEL_MAP[args.model]
        kwargs = {}

        if args.name:
            kwargs["name"] = args.name
        if args.group_id:
            kwargs["group_id"] = args.group_id
        if args.teacher_id:
            kwargs["teacher_id"] = args.teacher_id
        if args.subject_id:
            kwargs["subject_id"] = args.subject_id
        if args.student_id:
            kwargs["student_id"] = args.student_id
        if args.grade:
            kwargs["grade"] = args.grade
        if args.date:
            try:
                kwargs["date"] = datetime.strptime(args.date, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Incorrect date format! Vickory YYYY-MM-DD.")
                return

            if args.action == "create":
                obj = await create_object(session, model, **kwargs)
                print(f"✅ Created: {obj}")

            elif args.action == "list":
                objects = await list_objects(session, model)
                for obj in objects:
                    print(obj)

            elif args.action == "update":
                if not args.id:
                    print("❌ You need to pass --id for update.")
                    return
                obj = await update_object(session, model, args.id, **kwargs)
                if obj:
                    print(f"✅ Updated: {obj}")
                else:
                    print(f"❌ Object from ID {args.id} not found.")

            elif args.action == "remove":
                if not args.id:
                    print("❌You need to pass --id for display.")
                    return
                obj = await remove_object(session, model, args.id)
                if obj:
                    print(f"✅ Removed: {obj}")
                else:
                    print(f"❌ Object from ID {args.id} not found.")


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

    if top_stulent:
        print("="*50)
        print("Top 5 Students:")
        print("-" * 50)
        print(f"{'Name':<30}{'Avg Grade':<10}")
        print("-" * 50)
        for student in top_stulent:
            print(student)        
        print("="*50)
    if best_student:
        print("Best Student for 'Math':")
        print("-" * 50)
        print(f"{'Name':<30}{'Avg Grade':<10}")
        print("-" * 50)
        print(f"{best_student}")
        print("="*50)

    if avg_grade_by_group:
        print("Average Grade by Group for 'Math':")
        print("-" * 50)
        print(f"{'Group':<30}{'Avg Grade':<10}")
        print("-" * 50)
        for group, avg_grade in avg_grade_by_group:
            print(f"{group:<30}{avg_grade:<10.2f}")
        print("="*50)

    if avg_grade:
        print("Average Grade for the Entire Flow:")
        print("-" * 50)
        print(f"{'Avg Grade':<10}")
        print("-" * 50)
        print(f"{avg_grade:<10.2f}")
        print("="*50)

    if courses_by_teacher:
        print("Courses by Teacher:")
        print("-" * 50)
        print(f"{'Teacher':<30}{'Course':<30}")
        print("-" * 50)
        for teacher in courses_by_teacher:
            print(f"{teacher[0]}")
        print("="*50)

    if students_by_group:
        print("Students by Group:")
        print("-" * 50)
        print(f"{'Group':<30}{'Student'}")
        print("-" * 50)
        for  student in students_by_group:
            print(f"{student[0]}")
        print("="*50)

    if grades_by_group_and_subject:
        print("Grades by Group and Subject:")
        print("-" * 50)
        print(f"{'Group':<30}{'Subject':<30}")
        print("-" * 50)
        for group,  grade in grades_by_group_and_subject:
            print(f"{group:<30}{grade:<10}")
        print("="*50)

    if avg_grade_by_teacher:
        print("Average Grade by Teacher:")
        print("-" * 50)
        print(f"{'Teacher':<30}{'Avg Grade':<10}")
        print("-" * 50)
        if len(avg_grade_by_teacher) > 0:
            for teacher in avg_grade_by_teacher:
                print(f"{teacher}")
        print("="*50)


    if courses_by_student:
        print("Courses by Student:")
        print("-" * 50)
        print(f"{'Student':<30}")
        print("-" * 50)
        for student in courses_by_student:
            print(f"{student[0]}")
        print("="*50)

    if courses_by_student_and_teacher:
        print("Courses by Student and Teacher:")
        print("-" * 50)
        print(f"{'Student':<30}{'Teacher':<30}{'Course':<30}")
        print("-" * 50)
        for student, teacher, course in courses_by_student_and_teacher:
            print(f"{student:<30}{teacher:<30}{course:<30}")
        print("="*50)

if __name__ == '__main__':
    asyncio.run(main())


