from peewee import *
from src.models import ScheduleDate, Lesson


def init_db() -> SqliteDatabase:
    db = SqliteDatabase('data.db')
    db.create_tables([ScheduleDate, Lesson], safe=True)
    return db


def save_list_to_db(db: SqliteDatabase, raw_schedule: list) -> None:
    try:
        with db.atomic():
            for item in raw_schedule:
                date = ScheduleDate.create(
                    date=item['date'],
                    day_number=item['day_number'],
                    week_number=item['week_number']
                )
                lesson = Lesson.create(
                    date=date,
                    building=item['building'],
                    format=item['format'],
                    group=item['group'],
                    room=item['room'],
                    subject=item['subject'],
                    teacher_name=item['teacher_name'],
                    time_end=item['time_end'],
                    time_start=item['time_start'],
                    type=item['type'],
                    zoom_url=item['zoom_url'],
                    note=item['note']
                )
    except DoesNotExist as e:
        print(f"Data consistency error: {e}")
    except PeeweeException as e:
        print(f"Database error: {e}")

