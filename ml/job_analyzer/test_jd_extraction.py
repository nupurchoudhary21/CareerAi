from job_analyzer.jd_section_parser import parse_job_description
from job_analyzer.jd_skill_extractor import extract_skills_from_jd

test_descriptions = {
    "Software Engineer": """
    Experience in Web Testing.
    Experience in Functional, Integration, System testing.
    Experience in Manual Testing.
    Preparing and executing Test Cases.
    Knowledge of Database.
    """,

    "DevOps Engineer": """
    Job Title: Opening for Devops Engineer
    Skills Devops Engineer
    Required Skills
    Devops Engineer
    """
}

for title, description in test_descriptions.items():
    print(f"\n{title}")
    sections = parse_job_description(description)
    print("Sections:", sections)

    skills = extract_skills_from_jd(sections)
    print("Extracted skills:", skills)