import json
import re

skillsDict = {}

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE)

def extractSkills(file):
    with open(file) as data_file:
        data = json.load(data_file)

    for section in data["skills"]:
        for key in section:
            skillString = section[key]
            skillList = [skillList.strip() for skillList in re.split(',|:', skillString)]
    return skillList

from dateutil.parser import parse
from datetime import datetime

def extractDates(file, skillList):
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
            for x in skillList:
                print(x.lower())
                if re.search(r"[^a-z]"+re.escape(x.lower())+r"[^a-z]", text) != None:
                    skillsDict[x] += delta.total_seconds()
                    

filename = input("Filename: ")
skillList = extractSkills(filename)
for x in skillList:
  skillsDict[x] = 0
extractDates(filename, skillList)
for key in skillsDict:
    print(key)
    print(skillsDict[key])

