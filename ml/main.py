from resume_parser.pdf_parser import extract_text_from_pdf
from resume_parser.text_cleaner import clean_text
from resume_parser.contact_extractor import extract_contact_info

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

# Build skill evidence
skill_evidence = build_skill_evidence(
    profile,
    SKILL_ONTOLOGY
)


print("\n========== CONTACT INFORMATION ==========\n")
print(contact_info)

print("\n========== RESUME PROFILE ==========\n")
print(profile)

print("\n========== SKILL PROFILE ==========\n")
print(skill_profile)

print("\n========== ALL SKILLS ==========\n")
print(all_skills)

print("\n========== SKILL EVIDENCE ==========")

for skill, evidence in skill_evidence.items():

    print(f"\n{skill}")
    print(f"Category: {evidence['category']}")
    print(f"Sources: {evidence['sources']}")
    print(f"Confidence: {evidence['confidence']}")