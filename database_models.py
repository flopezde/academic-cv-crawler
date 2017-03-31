from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    name = CharField()


class Skill(BaseModel):
    skill_id = IntegerField(null=True)
    name = CharField(null=False)


class StudentSkill(Model):
    skill = ForeignKeyField(Skill, related_name="skills")
    student = ForeignKeyField(Student, related_name="students")
    weight = FloatField(null=False)

    class Meta:
        database = db
        primary_key = CompositeKey('skill', 'student')


class RawResume(BaseModel):
    resume_json = TextField()

if __name__ == '__main__':
    db.connect()
    db.create_tables([Student, Skill, StudentSkill, RawResume])
