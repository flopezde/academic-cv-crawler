import json
import re
from database_models import *
from dateutil.parser import parse
from datetime import datetime
from os import listdir, remove
from os.path import isfile, join


def find_whole_word(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE)


def extract_skills(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)

    for section in data["skills"]:
        for key in section:
            skill_string = section[key]
            skill_list = [skill_list.strip() for skill_list in re.split(',|:', skill_string)]
    return skill_list


def extract_dates(file, skill_list):
    with open(file) as data_file:
        data = json.load(data_file)

    for section in data["work_experience"]:
        delta = 0
        if "date_start" in section.keys():
            startDate = parse(section["date_start"])
        if "date_end" in section.keys():
            endDate = parse(section["date_end"])
        else:
            endDate = datetime.today()
        delta = endDate - startDate
        if "text" in section.keys():
            text = section["text"].lower()
            print(text)
            for x in skill_list:
                print(x.lower())
                if re.search(r"[^a-z]"+re.escape(x.lower())+r"[^a-z]", text) != None:
                    skillsDict[x] += delta.total_seconds()


def get_resume_files(resumes_dir):
    pdf_files = [f for f in listdir(resumes_dir) if (f[-4:] == '.pdf' and isfile(join(resumes_dir, f)))]
    return pdf_files


def save_skill_to_database(skill_name):
    if len(Skill.select().where(Skill.name == skill_name)) < 1:
        new_skill = Skill.create(name=skill_name)
        new_skill.skill_id = new_skill.id
        new_skill.save()


def parse_resume(resume, output):
    pass


def main(resumes_dir):
    pdf_files = get_resume_files(resumes_dir)
    temp_output_name = 'parsed.json'
    for resume in pdf_files:
        parse_resume(resume, temp_output_name)
        skills_list = extract_skills(temp_output_name)
        for skill_name in skills_list:
            save_skill_to_database(skill_name.lower())
        remove(temp_output_name)


filename = input("Filename: ")
skillList = extract_skills(filename)
skillsDict = dict()
for x in skillList:
  skillsDict[x] = 0
extract_dates(filename, skillList)
for key in skillsDict:
    print(key)
    print(skillsDict[key])

