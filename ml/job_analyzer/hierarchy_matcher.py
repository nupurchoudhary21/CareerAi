def find_related_resume_skills(
        jd_skill,
        resume_skills,
        skill_hierarchy
):
    related_skills = []

    relationship = skill_hierarchy.get(jd_skill)

    if not relationship:
        return related_skills

    children = relationship.get("children", [])

    for skill in children:
        if skill in resume_skills:
            related_skills.append(skill)

    return related_skills  


def find_parent_match(
        jd_skill,
        resume_skills,
        skill_hierarchy
):
    relationship = skill_hierarchy.get(jd_skill)

    if not relationship:
        return None

    parent = relationship.get("parent")

    if parent in resume_skills:
        return parent

    return None

def analyze_skill_relationship(
    jd_skill,
    resume_skills,
    skill_hierarchy
):
    if jd_skill in resume_skills:
        return {
            "direct_match": True,
            "related_skills": [],
            "parent_match": None
        }

    related_skills = find_related_resume_skills(
        jd_skill,
        resume_skills,
        skill_hierarchy
    )

    parent_match = find_parent_match(
        jd_skill,
        resume_skills,
        skill_hierarchy
    )

    return {
        "direct_match": False,
        "related_skills": related_skills,
        "parent_match": parent_match
    }

