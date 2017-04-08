#!/usr/bin/env python3
import argparse
from database_models import *
from raw_skill_extractor import parse_resume
from weighted_skill_extractor import extract_weighted_skills
from compatibility_score import compute_compatibility_score_for_all

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='different commands', dest='command')

    parser_add_job = subparsers.add_parser('add_job', help='add a new job')
    parser_add_job.add_argument('-t', '--title', dest='title', required=True, help='job title')
    parser_add_job.add_argument('-c', '--company', dest='company', required=True, help='name of the company')
    parser_add_job.add_argument('-s', '--skills', nargs='+', dest='skills', required=True,
                                help='required skill name, proficiency (out of 10) and importance (out of 10). '
                                     'Should be separated by  space, can include multiple skills')

    parser_add_resume = subparsers.add_parser('add_resume', help='add a new resume')
    parser_add_resume.add_argument('-f', '--file', dest='file', required=True, help='resume file')

    parser_compute = subparsers.add_parser('compute', help='computes compatibility score for every pair of jobs and '
                                                           'students')
    parser_compute.add_argument('-c', '--clear', dest='clear', help='clear database before computing',
                                action='store_true')

    parser_recommend = subparsers.add_parser('recommend', help='display recommendations')
    parser_recommend_type = parser_recommend.add_subparsers(help='type of entity to recommend to', dest='entity')

    parser_recommend_student = parser_recommend_type.add_parser('student', help='recommend students for a job')
    parser_recommend_student.add_argument('-t', '--title', dest='title', required=True, help='job title')
    parser_recommend_student.add_argument('-c', '--company', dest='company', required=True, help='name of the company')

    parser_recommend_job = parser_recommend_type.add_parser('job', help='recommend jobs for a student')
    parser_recommend_job.add_argument('-r', '--resume', dest='resume', required=True, help='file name of resume')

    # args = parser.parse_args("recommend student -t SE -c Google".split(' '))
    args = parser.parse_args()
    if args.command == 'add_job':
        if len(args.skills) % 3 != 0:
            raise Exception('skills should be multiply of 3')
        skills = list()
        for i in range(0, len(args.skills) - 2, 3):
            skills.append((args.skills[i], int(args.skills[i+1]), int(args.skills[i+2])))

        job = Job.create(title=args.title, company=args.company)
        for skill_tuple in skills:
            db_skill = Skill.select().where(Skill.name == skill_tuple[0]).get()
            if db_skill is not None:
                # weight is proficiency and importance
                weight = (skill_tuple[1] * skill_tuple[2]) / 100
                JobSkill.create(skill_id=db_skill.id, job=job, weight=weight)
    elif args.command == 'add_resume':
        resume = parse_resume(args.file)
        if resume is not None:
            extract_weighted_skills(resume)
    elif args.command == 'compute':
        if args.clear:
            CompatibilityScore.delete()
        compute_compatibility_score_for_all()
    elif args.command == 'recommend':
        if args.entity == 'student':
            jobs = Job.select().where(Job.title == args.title, Job.company == args.company)
            if len(jobs) == 0:
                print("Could not find the job on database")
            for db_job in jobs:
                c_scores = CompatibilityScore.select().where(CompatibilityScore.job == db_job)\
                    .order_by(CompatibilityScore.score.desc())
                if len(c_scores) == 0:
                    print("Could not find any matches. Please run compute first")
                for score in c_scores:
                    print('Score: {:0.2f}, Student: {}'.format(score.score, score.resume.file_name))
        elif args.entity == 'job':
            resumes = RawResume.select().where(RawResume.file_name.contains(args.resume))
            if len(resumes) == 0:
                print("Could not find the resume on database")
            for db_resume in resumes:
                c_scores = CompatibilityScore.select().where(CompatibilityScore.resume == db_resume)\
                    .order_by(CompatibilityScore.score.desc())
                if len(c_scores) == 0:
                    print("Could not find any matches. Please run compute first")
                for score in c_scores:
                    print('Score: {:0.2f}, Job: {} at {}'.format(score.score, score.job.title, score.job.company))

