import json
import re
from database_models import *
from dateutil.parser import parse as date_parser
from time import gmtime, strftime


def get_weight(start_date, end_date):
    duration = date_parser(end_date) - date_parser(start_date)
    max_months_experience = 12 * 10
    # Maximum weight of 1 for max_months_experience of experience
    # Minimum weight of .2 for no date
    experience_skill = (duration.days / 30) / max_months_experience
    experience_skill = max(.2, (experience_skill * .8) + .2)
    return min(experience_skill, 1.0)


def parse_work_experience(text, start_date, end_date, database_skill_list, resume):
    skills = list()
    for x in database_skill_list:
        if re.search(r"[^A-Za-z0-9]" + re.escape(x.name.lower()) + r"[^A-Za-z0-9]", text) is not None:
            skills.append(x)
    for skill_model in skills:
        try:
            weight = get_weight(start_date, end_date)
        except Exception as e:
            print(e)
            weight = .2
        try:
            ResumeSkill.create(skill_id=skill_model.skill_id, resume=resume, weight=weight)
        except IntegrityError as e:
            print(e)


def extract_weighted_skills(resume):
    database_skill_list = Skill.select()
    resume_json = json.loads(resume.resume_json)
    if "work_experience" in resume_json:
        for section in resume_json["work_experience"]:
            start_date = str()
            end_date = str()
            if "date_start" in section.keys():
                start_date = section["date_start"]
                if "date_end" in section.keys():
                    end_date = section["date_end"]
                else:
                    end_date = strftime("%d %b %Y", gmtime())
            if "text" in section.keys():
                text = section["text"].lower()
                parse_work_experience(text, start_date, end_date, database_skill_list, resume)
            else:
                for key, text in section.items():
                    parse_work_experience(text.lower(), "", "", database_skill_list, resume)

    if 'skills' in resume_json:
        ex_skills = list()
        for section in resume_json["skills"]:
            for key in section:
                skill_string = section[key].lower()
                for x in database_skill_list:
                    if re.search(r"[^A-Za-z0-9]"+re.escape(x.name.lower())+r"[^A-Za-z0-9]", skill_string) is not None:
                        ex_skills.append(x)
        for ex_skill in ex_skills:
            try:
                ResumeSkill.create(skill_id=ex_skill.skill_id, resume=resume, weight=.1)
            except IntegrityError as e:
                print(e)


def run():
    for resume in RawResume.select():
        extract_weighted_skills(resume)


if __name__ == '__main__':
    run()
