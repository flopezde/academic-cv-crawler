import json
import re

def extractSkills(file):
    with open(file) as data_file:
        data = json.load(data_file)

    for section in data["skills"]:
        for key in section:
            skillString = section[key]
            skillList = [skillList.strip() for skillList in re.split(',|:', skillString)]

    for x in skillList:
        print(x)

extractSkills(input("Filename: "))
