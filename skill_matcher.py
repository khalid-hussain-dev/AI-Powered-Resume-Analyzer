def load_skills(job_role_file):
    with open(job_role_file, 'r') as file:
        skills = file.read().splitlines()
    return set(skill.lower() for skill in skills)

def match_skills(resume_tokens, job_skills):
    matched = resume_tokens & job_skills
    missing = job_skills - resume_tokens
    match_percent = round((len(matched) / len(job_skills)) * 100, 2)
    return matched, missing, match_percent
