from utils.job_roles import JOB_ROLES

def match_role(role, skills):

    required = JOB_ROLES.get(role, [])

    found = []

    missing = []

    for skill in required:

        if skill in skills:
            found.append(skill)
        else:
            missing.append(skill)

    if len(required) == 0:
        match = 0
    else:
        match = int((len(found) / len(required)) * 100)

    return match, found, missing
