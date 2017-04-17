from database_models import *


def get_resume_skills(resume):
    resume_skills = ResumeSkill.select().where(ResumeSkill.resume == resume)
    weighted_skills = dict()
    for skill in resume_skills:
        weighted_skills[skill.skill_id] = skill.weight
    return weighted_skills


def get_job_skills(job):
    job_skills = JobSkill.select().where(JobSkill.job == job)
    weighted_skills = dict()
    for skill in job_skills:
        weighted_skills[skill.skill_id] = skill.weight
    return weighted_skills


def compute_compatibility_score_for_all():
    all_resume_skills = dict()
    all_job_skills = dict()
    for resume in RawResume.select():
        all_resume_skills[resume.id] = get_resume_skills(resume)
    for job in Job.select():
        all_job_skills[job.id] = get_job_skills(job)

    for resume_id, resume_skills in all_resume_skills.items():
        for job_id, job_skills in all_job_skills.items():
            compatibility_score = 0.
            for skill_id in resume_skills:
                if skill_id in job_skills:
                    compatibility_score += resume_skills[skill_id] * job_skills[skill_id]
            compatibility_score /= len(all_job_skills[job_id])
            CompatibilityScore.create(job=job_id, resume=resume_id, score=compatibility_score)


def run():
    compute_compatibility_score_for_all()


if __name__ == '__main__':
    run()
