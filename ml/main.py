from resume_parser.pdf_parser import extract_text_from_pdf
from resume_parser.text_cleaner import clean_text
from resume_parser.contact_extractor import extract_contact_info
from resume_parser.skill_strength import build_skill_strength
from resume_parser.profile_builder import build_final_skill_profile


from resume_parser.skill_extractor import (
    extract_skills_from_profile,
    get_all_skills,
    SKILL_ONTOLOGY
)

from resume_parser.section_parser import (
    parse_sections,
    create_resume_profile,
    extract_name
)

from resume_parser.skill_evidence import build_skill_evidence

from resume_parser.skill_hierarchy import (
    build_skill_hierarchy,
    deduplicate_skills
)


pdf_path = "../datasets/resumes/resume2.pdf"

raw_text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(raw_text)

contact_info = extract_contact_info(cleaned_text)

name = extract_name(cleaned_text)

sections = parse_sections(cleaned_text)

profile = create_resume_profile(sections, name)


print("\n========== TEXT SENT TO SKILL EXTRACTOR ==========\n")

for section in ["skills", "projects"]:
    print(f"\n--- {section.upper()} ---")
    print(profile.get(section, []))


# Extract skills
skill_profile = extract_skills_from_profile(profile)

# Flatten skills into one list
all_skills = get_all_skills(skill_profile)

# Remove duplicate skills
unique_skills = deduplicate_skills(all_skills)


# Build skill evidence
skill_evidence = build_skill_evidence(
    profile,
    SKILL_ONTOLOGY
)

# Build skill hierarchy
skill_hierarchy = build_skill_hierarchy(
    unique_skills
)

skill_evidence = build_skill_evidence(
    profile,
    SKILL_ONTOLOGY
)

skill_strength = build_skill_strength(
    skill_evidence
)

skill_hierarchy = build_skill_hierarchy(
    unique_skills
)

final_skill_profile = build_final_skill_profile(
    skill_profile,
    skill_evidence,
    skill_strength,
    skill_hierarchy
)

print("\n========== SKILL HIERARCHY ==========")

for skill, relationship in skill_hierarchy.items():

    print(f"\n{skill}")
    print(f"Parent: {relationship['parent']}")
    print(f"Children: {relationship['children']}")


print("\n========== CONTACT INFORMATION ==========\n")
print(contact_info)

print("\n========== RESUME PROFILE ==========\n")
print(profile)

print("\n========== SKILL PROFILE ==========\n")
print(skill_profile)

print("\n========== ALL SKILLS ==========\n")
print(all_skills)

print("\n========== SKILL HIERARCHY ==========")

for skill, relationship in skill_hierarchy.items():

    print(f"\n{skill}")
    print(f"Parent: {relationship['parent']}")
    print(f"Children: {relationship['children']}")

print("\n========== SKILL EVIDENCE ==========")

for skill, evidence in skill_evidence.items():

    print(f"\n{skill}")
    print(f"Category: {evidence['category']}")
    print(f"Sources: {evidence['sources']}")
    print(f"Explicit: {evidence['explicit']}")
    print(f"Inferred: {evidence['inferred']}")
    print(f"Confidence: {evidence['confidence']}")


print("\n========== SKILL STRENGTH ==========")

for skill, strength in skill_strength.items():

    print(f"\n{skill}")
    print(f"Score: {strength['score']}")
    print(f"Level: {strength['level']}")    


print("\n========== FINAL SKILL PROFILE ==========")

for skill, data in final_skill_profile.items():

    print(f"\n{skill}")

    print(f"Category: {data['category']}")

    print(
        f"Sources: "
        f"{data['evidence'].get('sources', [])}"
    )

    print(
        f"Confidence: "
        f"{data['evidence'].get('confidence')}"
    )

    print(
        f"Strength: "
        f"{data['strength'].get('score')}"
    )

    print(
        f"Level: "
        f"{data['strength'].get('level')}"
    )

    print(
        f"Parent: "
        f"{data['hierarchy'].get('parent')}"
    )

    print(
        f"Children: "
        f"{data['hierarchy'].get('children', [])}"
    )    



# job analyse 


from job_analyzer.jd_cleaner import clean_job_description
from job_analyzer.jd_section_parser import parse_job_description
from job_analyzer.jd_skill_extractor import extract_skills_from_jd
from job_analyzer.jd_profile_builder import build_jd_profile
from job_analyzer.skill_matcher import match_skills

jd_text = """
Software Engineer

Requirements:
- Strong Python and JavaScript
- Experience with React and Node.js
- Knowledge of MongoDB
- Good problem solving skills

Preferred:
- Docker
- FastAPI
- AWS

Responsibilities:
- Build REST APIs
- Develop web applications
- Work with databases
"""

cleaned_jd = clean_job_description(jd_text)

jd_sections = parse_job_description(cleaned_jd)

jd_skills = extract_skills_from_jd(jd_sections)

jd_profile = build_jd_profile(
    jd_sections,
    jd_skills
)

# print("\n--- JD SECTIONS ---")
# print(jd_sections)

# print("\n--- JD SKILLS ---")
# print(jd_skills)

# print("\n--- JD PROFILE ---")
# print(jd_profile)


resume_skills = get_all_skills(skill_profile)

skill_match = match_skills(
    resume_skills,
    jd_profile
)

print("\n--- SKILL MATCH ---")
print(skill_match)
 