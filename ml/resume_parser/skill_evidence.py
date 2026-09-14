from .skill_extractor import skill_found_in_text


def calculator_confidence(sources):
    if "skills" in sources and (
        "projects" in sources
        or "experience" in sources
        or "internships" in sources
    ):
        return "very high"

    if "skills" in sources:
        return "high"

    if(
        "projects" in sources
        or "experience" in sources
        or "internships" in sources
    ):
        return "medium"

    return "low"


def build_skill_evidence(profile, skill_onotology):
    """
    find where each skill appears in the resume and assign an evidence confidence level
    """

    sections = {
        "skills": profile.get("skills", []),
        "projects": profile.get("projects", []),
        "experience": profile.get("experience", []),
        "internships": profile.get("internships", []),
        "research": profile.get("research", []),
        "coursework": profile.get("coursework", [])
    }

    skill_evidence = {}

    for category, skills in skill_onotology.items():
        for canonical_name, aliases in skills.items():

            sources =[]

            for section_name, section_data in sections.items():
                if not section_data:
                    continue

                if isinstance(section_data, list):
                    section_text = " ".join(section_data)

                else:
                    section_text = str(section_data)

                if skill_found_in_text(
                    section_text,
                    aliases
                ):
                    sources.append(section_name)

            if sources:

                explicit = "skills" in sources

                inferred = any(
                    source in sources 
                    for source in [
                        "projects",
                        "experience",
                        "internships",
                        "research"
                    ]
                )

                skill_evidence[canonical_name] = {
                    "category": category,
                    "sources": sources,
                    "explicit": explicit,
                    "inferred": inferred,
                    "confidence": calculator_confidence(sources)
                }              

    return skill_evidence
