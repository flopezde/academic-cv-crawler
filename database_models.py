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
    skill_id = IntegerField()
    name = CharField(null=False)


class StudentSkill(BaseModel):
    skill = ForeignKeyField(Skill, related_name="skills")
    student = ForeignKeyField(Student, related_name="students")
    weight = FloatField(null=False)


if __name__ == '__main__':
    db.connect()
    db.create_tables([Student, Skill, StudentSkill])
