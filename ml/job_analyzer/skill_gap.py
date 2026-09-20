def build_skill_gap(
    skill_match,
    related_match
):

    critical_gaps = skill_match["missing_required"]
    preferred_gaps = skill_match["missing_preferred"]

    matched_skills = (
        skill_match["matched_required"]
        + skill_match["matched_preferred"]
    )

    extra_skills = skill_match["extra_skills"]

    related_critical_gaps = {}
    related_preferred_gaps = {}

    # Analyze related skills for missing required skills
    for skill in critical_gaps:

        related_data = related_match["required"].get(
            skill,
            {}
        )

        if related_data.get("related_match"):

            related_critical_gaps[skill] = {
                "related_skills": related_data.get(
                    "related_skills",
                    []
                )
            }

    # Analyze related skills for missing preferred skills
    for skill in preferred_gaps:

        related_data = related_match["preferred"].get(
            skill,
            {}
        )

        if related_data.get("related_match"):

            related_preferred_gaps[skill] = {
                "related_skills": related_data.get(
                    "related_skills",
                    []
                )
            }

    return {
        "critical_gaps": critical_gaps,
        "preferred_gaps": preferred_gaps,
        "matched_skills": matched_skills,
        "extra_skills": extra_skills,
        "related_critical_gaps": related_critical_gaps,
        "related_preferred_gaps": related_preferred_gaps
    }