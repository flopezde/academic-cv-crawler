from os import listdir, remove, chdir, system
from os.path import isfile, join
from database_models import *


def get_resume_files(resumes_dir):
    pdf_files = [join(resumes_dir, f) for f in listdir(resumes_dir) if (f[-4:] == '.pdf' and isfile(join(resumes_dir, f)))]
    return pdf_files


def parse_resume_to_json(relative_resume_path, output):
    chdir('ResumeParser/ResumeTransducer')
    system('export GATE_HOME="../GATEFiles"')
    command = ("java -cp 'bin/*:../GATEFiles/lib/*:../GATEFiles/bin/gate.jar:lib/*' "
               "code4goal.antony.resumeparser.ResumeParserProgram "
               "../../" + relative_resume_path + " "
               "../../" + output)
    system(command)
    chdir('../..')


def parse_resume(relative_resume_path):
    temp_output_name = 'parsed.json'
    parse_resume_to_json(relative_resume_path, temp_output_name)
    with open(temp_output_name, 'r') as json_file:
        result = RawResume.create(resume_json=json_file.read(), file_name=relative_resume_path)
    remove(temp_output_name)
    return result


def parse_directory(resumes_dir):
    pdf_files = get_resume_files(resumes_dir)
    for resume_file in pdf_files:
        parse_resume(resume_file)