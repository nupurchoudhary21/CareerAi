def build_jd_profile(
        sections,
        extracted_skills
):
    return{
        "required": {
            "text": sections.get("required", []),
            "skills": extracted_skills.get("required", [])
        },

        "preferred": {
            "text": sections.get("preferred", []),
            "skills": extracted_skills.get("preferred", [])
        },

        "responsibilities": {
            "text": sections.get("responsibilities", []),
            "skills": extracted_skills.get("responsibilities", [])
        }
    } 