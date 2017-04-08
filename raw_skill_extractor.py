import json
import re
from resume_parser import *


def find_whole_word(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE)


def extract_skills(resume_json):
    if 'skills' in resume_json:
        skill_list = list()
        for section in resume_json["skills"]:
            for key in section:
                skill_string = section[key]
                skill_list += [y for y in [x.replace("\n", "").strip() for x in re.split("\s*[^A-Za-z0-9\s+\-\(\)]\s*",
                                                                                         skill_string)] if y != '']
        return skill_list


def save_skill_to_database(skill_name):
    if len(RawSkill.select().where(RawSkill.name == skill_name)) < 1:
        RawSkill.create(name=skill_name)


if __name__ == '__main__':
    if len(RawResume.select()) < 1:
        parse_directory('resumes')

    for resume in RawResume.select():
        resume_json = json.loads(resume.resume_json)
        skills_list = extract_skills(resume_json)
        if skills_list is not None:
            for skill_name in skills_list:
                save_skill_to_database(skill_name.lower())
        else:
            print("No skills!")
