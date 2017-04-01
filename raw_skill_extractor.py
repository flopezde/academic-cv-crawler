import json
import re
from database_models import *
from os import listdir, remove, chdir, system
from os.path import isfile, join


def find_whole_word(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE)


def extract_skills(resume_json):
    if 'skills' in resume_json:
        skill_list = list()
        for section in resume_json["skills"]:
            for key in section:
                skill_string = section[key]
                skill_list += [y for y in [x.replace("\n", "").strip() for x in re.split("\s*[^A-Za-z0-9\s+\-\(\)]\s*", skill_string)] if y != '']
        return skill_list


def get_resume_files(resumes_dir):
    pdf_files = [join(resumes_dir, f) for f in listdir(resumes_dir) if (f[-4:] == '.pdf' and isfile(join(resumes_dir, f)))]
    return pdf_files


def save_skill_to_database(skill_name):
    if len(RawSkill.select().where(RawSkill.name == skill_name)) < 1:
        RawSkill.create(name=skill_name)


def parse_resume(resume, output):
    chdir('ResumeParser/ResumeTransducer')
    system('export GATE_HOME="../GATEFiles"')
    command = ("java -cp 'bin/*:../GATEFiles/lib/*:../GATEFiles/bin/gate.jar:lib/*' "
               "code4goal.antony.resumeparser.ResumeParserProgram "
               "../../" + resume + " "
               "../../" + output)
    system(command)
    chdir('../..')


def parse_directory(resumes_dir):
    pdf_files = get_resume_files(resumes_dir)
    temp_output_name = 'parsed.json'
    for resume_file in pdf_files:
        parse_resume(resume_file, temp_output_name)
        with open(temp_output_name, 'r') as json_file:
            RawResume.create(resume_json=json_file.read())
        remove(temp_output_name)


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
