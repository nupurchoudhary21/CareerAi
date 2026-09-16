def match_skills(resume_skills, jd_profile):

    required_skills = jd_profile["required"]["skills"]
    preferred_skills = jd_profile["preferred"]["skills"]

    matched_required = []
    missing_required = []

    matched_preferred = []
    missing_preferred = []

    for skill in required_skills:
        if skill in resume_skills:
            matched_required.append(skill)
        else:
            missing_required.append(skill)


    for skill in preferred_skills:
        if skill in resume_skills:
            matched_preferred.append(skill)

        else:
            missing_preferred.append(skill)

    jd_skills = set(required_skills + preferred_skills)

    extra_skills = [
        skill
        for skill in resume_skills
        if skill not in jd_skills
    ]

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "extra_skills": extra_skills
    }                        