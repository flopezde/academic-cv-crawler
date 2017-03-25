import json
import re
from database_models import *
from os import listdir, remove, chdir, system
from os.path import isfile, join


def find_whole_word(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE)


def extract_skills(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)

    if 'skills' in data:
        skill_list = list()
        for section in data["skills"]:
            for key in section:
                skill_string = section[key]
                skill_list += [x.strip() for x in re.split(',|:', skill_string)]
        return skill_list


def get_resume_files(resumes_dir):
    pdf_files = [join(resumes_dir, f) for f in listdir(resumes_dir) if (f[-4:] == '.pdf' and isfile(join(resumes_dir, f)))]
    return pdf_files


def save_skill_to_database(skill_name):
    if len(Skill.select().where(Skill.name == skill_name)) < 1:
        new_skill = Skill.create(name=skill_name)
        new_skill.skill_id = new_skill.id
        new_skill.save()


def parse_resume(resume, output):
    chdir('ResumeParser/ResumeTransducer')
    system('export GATE_HOME="..\GATEFiles"')
    command = ("java -cp 'bin/*:../GATEFiles/lib/*:../GATEFiles/bin/gate.jar:lib/*' "
               "code4goal.antony.resumeparser.ResumeParserProgram "
               "../../" + resume + " "
               "../../" + output)
    system(command)
    chdir('../..')


def run(resumes_dir):
    pdf_files = get_resume_files(resumes_dir)
    temp_output_name = 'parsed.json'
    for resume in pdf_files:
        parse_resume(resume, temp_output_name)
        skills_list = extract_skills(temp_output_name)
        if skills_list is not None:
            for skill_name in skills_list:
                save_skill_to_database(skill_name.lower())
        else:
            print("No skills!")
        remove(temp_output_name)

if __name__ == '__main__':
    run('CVs')
