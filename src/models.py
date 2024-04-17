from peewee import Model, SqliteDatabase, DateField, IntegerField, ForeignKeyField, TextField, AutoField


class BaseModel(Model):
    class Meta:
        database = db


class ScheduleDate(BaseModel):
    id = AutoField(primary_key=True)
    date = DateField()
    day_number = IntegerField()
    week_number = IntegerField()


class Lesson(ScheduleDate):
    date = ForeignKeyField(ScheduleDate, backref='lessons')
    building = TextField(null=True)
    format = TextField(null=True)
    group = TextField(null=True)
    room = TextField(null=True)
    subject = TextField(null=True)
    teacher_name = TextField(null=True)
    time_end = TextField(null=True)
    time_start = TextField(null=True)
    type = TextField(null=True)
    zoom_url = TextField(null=True)
    note = TextField(null=True)

