RELATED_SKILLS = {
    "Django": [
        "Flask"
    ],

    "Flask": [
        "Django"
    ],

    "React": [
        "Angular",
        "Vue.js"
    ],

    "Angular": [
        "React",
        "Vue.js"
    ],

    "Vue.js": [
        "React",
        "Angular"
    ],

    "MySQL": [
        "PostgreSQL",
        "SQLite"
    ],

    "PostgreSQL": [
        "MySQL",
        "SQLite"
    ],

    "MongoDB": [
        "Redis"
    ],

    "AWS": [
        "Microsoft Azure",
        "Google Cloud Platform"
    ],

    "Microsoft Azure": [
        "AWS",
        "Google Cloud Platform"
    ],

    "Google Cloud Platform": [
        "AWS",
        "Microsoft Azure"
    ]

}

def get_related_skills(skill):
    return RELATED_SKILLS.get(skill, [])

def find_related_resume_skills(
        jd_skill,
        resume_skills
):
    related_skills = []

    related_candidates = get_related_skills(
        jd_skill,
    )

    for skill in related_candidates:
        if skill in resume_skills:
            related_skills.append(skill)

    return related_skills


def analyze_related_skill_match(
        jd_skill,
        resume_skills
):

    if jd_skill in resume_skills:

        return {
            "direct_match": True,
            "related_match": False,
            "related_skills": []
        }

    related_skills = find_related_resume_skills(
        jd_skill,
        resume_skills
    )

    return {
        "direct_match": False,
        "related_match": len(related_skills) > 0,
        "related_skills": related_skills
    }

