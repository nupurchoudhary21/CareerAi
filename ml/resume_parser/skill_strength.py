def calculate_skill_strength(evidence):

    score = 0.0

    sources = evidence["sources"]

    if "skills" in sources:
        score += 0.30

    if "projects" in sources:
        score += 0.30

    if "experience" in sources:
        score += 0.30

    if "internships" in sources:
        score += 0.30

    if "research" in sources:
        score += 0.20

    return min(score, 1.0)

def strength_level(score):

    if score >= 0.75:
        return "strong"

    if score >= 0.50:
        return "moderate"

    if score >= 0.25:
        return "basic"

    return "weak"


def build_skill_strength(skill_evidence):

    skill_stength = {}

    for skill, evidence in skill_evidence.items():
        score = calculate_skill_strength(evidence)

        skill_stength[skill] = {
            "score" : round(score,2),
            "level": strength_level(score)
        }

    return skill_stength    

