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
    file_name = CharField()


class ResumeSkill(Model):
    skill_id = IntegerField(null=True)
    resume = ForeignKeyField(RawResume, related_name="skill_resumes")
    weight = FloatField(null=False)

    class Meta:
        database = db
        primary_key = CompositeKey('skill_id', 'resume')


class Job(BaseModel):
    name = CharField()


class JobSkill(Model):
    skill_id = IntegerField(null=True)
    job = ForeignKeyField(Job, related_name="skill_jobs")
    weight = FloatField(null=False)

    class Meta:
        database = db
        primary_key = CompositeKey('skill_id', 'job')


class CompatibilityScore(Model):
    job = ForeignKeyField(RawResume, related_name="compatibility_jobs")
    resume = ForeignKeyField(RawResume, related_name="compatibility_resumes")
    score = FloatField(null=False)

    class Meta:
        database = db
        primary_key = CompositeKey('job', 'resume')


if __name__ == '__main__':
    db.connect()
    db.create_tables([Student, RawSkill, Skill, RawResume, ResumeSkill, Job, JobSkill, CompatibilityScore])
