import json
import re
from database_models import *
from dateutil.parser import parse as date_parser
from datetime import datetime
from os import listdir, remove, chdir, system
from os.path import isfile, join


def get_weight(start_date, end_date):
    duration = date_parser(end_date) - date_parser(start_date)
    dir(duration)
    return duration


def extract_dates(resume, skill_list):
    resume_json = json.loads(resume.resume_json)
    if "work_experience" in resume_json:
        for section in resume_json["work_experience"]:
            start_date = str()
            end_date = str()
            if "date_start" in section.keys():
                start_date = section["date_start"]
                if "date_end" in section.keys():
                    end_date = section["date_end"]
            if "text" in section.keys():
                text = section["text"].lower()
                skills = list()
                for x in skill_list:
                    if re.search(r"[^A-Za-z0-9]"+re.escape(x.name.lower())+r"[^A-Za-z0-9]", text) is not None:
                        skills.append(x)
                for skill_model in skills:
                    try:
                        weight = get_weight(start_date, end_date)
                    except Exception as e:
                        print(e)
                        weight = 0
                    StudentSkill.create(skill=skill_model, resume=resume, weight=weight)


def run():
    skills = Skill.select()
    for resume in RawResume.select():
        extract_dates(resume, skills)


if __name__ == '__main__':
    run()
