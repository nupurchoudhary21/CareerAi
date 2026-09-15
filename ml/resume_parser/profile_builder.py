def build_final_skill_profile(
        skill_profile,
        skill_evidence,
        skill_strength,
        skill_hierarchy
):
    """
    combine all skill information into one structured profile
    """

    final_profile = {}

    for category, skills in skill_profile.items():
        for skill in skills:

            final_profile = {}

            for category, skills in skill_profile.items():

                for skill in skills:

                    final_profile[skill] = {
                        "category": category,

                        "evidence": skill_evidence.get(
                            skill,
                            {}
                        ),

                        "strength": skill_strength.get(
                            skill,
                            {}
                        ),

                        "hierarchy": skill_hierarchy.get(
                            skill,
                            {}
                        )
                    }

    return final_profile        