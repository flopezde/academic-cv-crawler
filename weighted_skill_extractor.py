import json
import re
from database_models import *
from dateutil.parser import parse
from datetime import datetime
from os import listdir, remove, chdir, system
from os.path import isfile, join


def get_weight(start_date, end_date):
    duration = parse(end_date) - parse(start_date)

def extract_dates(json_file, skill_list):
    with open(json_file) as data_file:
        data = json.load(data_file)

    if "work_experience" in data:
        for section in data["work_experience"]:
            if "date_start" in section.keys():
                start_date = section["date_start"]
                if "date_end" in section.keys():
                    end_date = section["date_end"]
            if "text" in section.keys():
                text = section["text"].lower()
                skills = list()
                for x in skill_list:
                    if re.search(r"[^a-z]"+re.escape(x.skill_name.lower())+r"[^a-z]", text) is not None:
                        skills.append(x)
                for skill_model in skills:
                    weight = get_weight(start_date, end_date)
                    StudentSkill.create(skill=skill_model,student=)




def get_resume_files(resumes_dir):
    pdf_files = [f for f in listdir(resumes_dir) if (f[-4:] == '.pdf' and isfile(join(resumes_dir, f)))]
    return pdf_files


def parse_resume(resume, output):
    chdir('ResumeParser/ResumeTransducer')
    system('export GATE_HOME="../GATEFiles"')
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
        extract_dates(temp_output_name, Skill.select())
        remove(temp_output_name)


if __name__ == '__main__':
    run('resumes')