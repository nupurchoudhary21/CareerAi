def build_evidence_aware_match(
    resume_skill_profile,
    jd_profile
):
    required_skills = jd_profile["required"]["skills"]
    preferred_skills = jd_profile["preferred"]["skills"]

    required = {}
    preferred = {}

    for skill in required_skills:

        if skill in resume_skill_profile:

            skill_data = resume_skill_profile[skill]

            required[skill] = {
                "matched": True,
                "confidence": skill_data["evidence"].get(
                    "confidence"
                ),
                "strength": skill_data["strength"].get(
                    "level"
                ),
                "sources": skill_data["evidence"].get(
                    "sources",
                    []
                )
            }

        else:

            required[skill] = {
                "matched": False,
                "confidence": None,
                "strength": None,
                "sources": []
            }

    for skill in preferred_skills:

        if skill in resume_skill_profile:

            skill_data = resume_skill_profile[skill]

            preferred[skill] = {
                "matched": True,
                "confidence": skill_data["evidence"].get(
                    "confidence"
                ),
                "strength": skill_data["strength"].get(
                    "level"
                ),
                "sources": skill_data["evidence"].get(
                    "sources",
                    []
                )
            }

        else:

            preferred[skill] = {
                "matched": False,
                "confidence": None,
                "strength": None,
                "sources": []
            }

    return {
        "required": required,
        "preferred": preferred
    }