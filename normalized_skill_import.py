from database_models import *

file_name = 'normalized_skills.txt'
with open(file_name, 'r') as file:
    for line in file.readlines():
        _id, skill_id, skill_name = line.split("|")
        try:
            Skill.create(skill_id=skill_id, name=skill_name.strip())
        except Exception as e:
            print(e)
