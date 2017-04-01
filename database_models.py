from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    name = CharField()


class RawSkill(BaseModel):
    name = CharField(null=False)


class Skill(BaseModel):
    skill_id = IntegerField(null=True)
    name = CharField(null=False, unique=True)


class RawResume(BaseModel):
    resume_json = TextField()


class StudentSkill(Model):
    skill = ForeignKeyField(Skill, related_name="skills")
    resume = ForeignKeyField(RawResume, related_name="resumes")
    weight = FloatField(null=False)

    class Meta:
        database = db
        primary_key = CompositeKey('skill', 'resume')


if __name__ == '__main__':
    db.connect()
    db.create_tables([Student, Skill, RawResume, StudentSkill])
