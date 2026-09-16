def build_skill_gap(skill_match):

    critical_gaps = skill_match["missing_required"]
    preferred_gaps =  skill_match["missing_preferred"]

    matched_skills = (
        skill_match["matched_required"]
        + skill_match["matched_preferred"]
    )

    return{
        "critical_gaps": critical_gaps,
        "preferred_gaps": preferred_gaps,
        "matched_skills": matched_skills,
        "extra_skills": skill_match["extra_skills"]
    }