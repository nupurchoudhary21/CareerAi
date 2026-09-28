from resume_parser.skill_extractor import (
    skill_found_in_text,
    SKILL_ONTOLOGY
)

text = """
Experience in Web Testing.
Experience in Functional, Integration, System testing.
Experience in Manual Testing.
Preparing and executing Test Cases.
Knowledge of Database.
Devops Engineer
"""

test_skills = [
    "Manual Testing",
    "Integration Testing",
    "System Testing",
    "Functional Testing",
    "Test Cases",
    "Database",
    "DevOps"
]

for skill in test_skills:
    found = False

    for category, skills in SKILL_ONTOLOGY.items():
        if skill in skills:
            aliases = skills[skill]
            found = skill_found_in_text(text, aliases)
            print(f"{skill}: {found}")
            break

    if not found and not any(
        skill in skills for skills in SKILL_ONTOLOGY.values()
    ):
        print(f"{skill}: Not found in ontology")