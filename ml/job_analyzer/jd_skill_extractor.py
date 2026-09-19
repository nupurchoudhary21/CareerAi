from resume_parser.skill_extractor import (
    skill_found_in_text,
    SKILL_ONTOLOGY
)


def extract_skills_from_jd(sections):

    result = {
        "required": [],
        "preferred": [],
        "responsibilities": []
    }

    for section_name, section_data in sections.items():

        if section_name not in result:
            continue

        section_text = " ".join(section_data)

        print("\nCHECKING SECTION:", section_name)
        print("SECTION TEXT:", section_text)

        for category, skills in SKILL_ONTOLOGY.items():

            for canonical_name, aliases in skills.items():

                if skill_found_in_text(
                    section_text,
                    aliases
                ):

                    print(
                        "EXTRACTOR FOUND:",
                        canonical_name
                    )

                    if canonical_name not in result[section_name]:

                        result[section_name].append(
                            canonical_name
                        )

    return result