# ==========================================
# RESUME PARSER
# ==========================================

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

from resume_parser.skill_evidence import (
    build_skill_evidence
)

from resume_parser.skill_hierarchy import (
    build_skill_hierarchy,
    deduplicate_skills
)


# ==========================================
# JOB ANALYZER
# ==========================================

from job_analyzer.job_loader import load_jobs
from job_analyzer.jd_cleaner import clean_job_description
from job_analyzer.jd_section_parser import parse_job_description
from job_analyzer.jd_skill_extractor import extract_skills_from_jd
from job_analyzer.jd_profile_builder import build_jd_profile


# ==========================================
# MATCHING
# ==========================================

from job_analyzer.unified_matcher import (
    build_unified_match
)


# ==========================================
# 1. PROCESS RESUME
# ==========================================

pdf_path = "../datasets/resumes/resume2.pdf"

raw_text = extract_text_from_pdf(
    pdf_path
)

cleaned_text = clean_text(
    raw_text
)

contact_info = extract_contact_info(
    cleaned_text
)

name = extract_name(
    cleaned_text
)

sections = parse_sections(
    cleaned_text
)

profile = create_resume_profile(
    sections,
    name
)


# ==========================================
# 2. EXTRACT RESUME SKILLS
# ==========================================

skill_profile = extract_skills_from_profile(
    profile
)

all_skills = get_all_skills(
    skill_profile
)

unique_skills = deduplicate_skills(
    all_skills
)


# ==========================================
# 3. RESUME EVIDENCE
# ==========================================

skill_evidence = build_skill_evidence(
    profile,
    SKILL_ONTOLOGY
)


# ==========================================
# 4. RESUME STRENGTH
# ==========================================

skill_strength = build_skill_strength(
    skill_evidence
)


# ==========================================
# 5. RESUME HIERARCHY
# ==========================================

skill_hierarchy = build_skill_hierarchy(
    unique_skills
)


# ==========================================
# 6. FINAL RESUME SKILL PROFILE
# ==========================================

final_skill_profile = build_final_skill_profile(
    skill_profile,
    skill_evidence,
    skill_strength,
    skill_hierarchy
)


print("\n========== RESUME ==========")
print("Name:", name)

print("\nResume Skills:")
print(unique_skills)


# ==========================================
# 7. LOAD JOB DATASET
# ==========================================

jobs = load_jobs(
    "../datasets/jobs/jobs.csv"
)

print("\nTotal Jobs:", len(jobs))


# ==========================================
# 8. TEST ONE JOB
# ==========================================

job = jobs[1]

print("\n========== SELECTED JOB ==========")
print("Title:", job["job_title"])


# ==========================================
# 9. CLEAN JD
# ==========================================

cleaned_jd = clean_job_description(
    job["job_description"]
)


# ==========================================
# 10. PARSE JD
# ==========================================

jd_sections = parse_job_description(
    cleaned_jd
)

print("\n========== DIRECT JD SKILL TEST ==========")

test_text = " ".join(jd_sections["required"])

from resume_parser.skill_extractor import SKILL_ONTOLOGY
from resume_parser.skill_extractor import skill_found_in_text

for category, skills in SKILL_ONTOLOGY.items():

    for canonical_name, aliases in skills.items():

        if skill_found_in_text(test_text, aliases):
            print("FOUND:", canonical_name)


print("\n========== JD SECTIONS ==========")

print("\nREQUIRED:")
print(jd_sections["required"])

print("\nPREFERRED:")
print(jd_sections["preferred"])

print("\nRESPONSIBILITIES:")
print(jd_sections["responsibilities"])


# ==========================================
# 11. EXTRACT JD SKILLS
# ==========================================

jd_skills = extract_skills_from_jd(
    jd_sections
)


# ==========================================
# 12. BUILD JD PROFILE
# ==========================================

jd_profile = build_jd_profile(
    jd_sections,
    jd_skills
)


print("\n========== JD PROFILE ==========")

print("\nRequired Skills:")
print(jd_profile["required"]["skills"])

print("\nPreferred Skills:")
print(jd_profile["preferred"]["skills"])

print("\nResponsibility Skills:")
print(
    jd_profile["responsibilities"]["skills"]
)


# ==========================================
# 13. UNIFIED MATCH
# ==========================================

unified_match = build_unified_match(
    unique_skills,
    final_skill_profile,
    jd_profile,
    skill_hierarchy
)


# ==========================================
# 14. PRINT MATCH RESULT
# ==========================================

print("\n========== MATCH SCORE ==========")

print(
    unified_match["match_score"]
)


print("\n========== SKILL MATCH ==========")

print(
    unified_match["skill_match"]
)


print("\n========== SKILL GAP ==========")

print(
    unified_match["skill_gap"]
)


print("\n========== EVIDENCE MATCH ==========")

print(
    unified_match["evidence_match"]
)


print("\n========== HIERARCHY MATCH ==========")

print(
    unified_match["hierarchy_match"]
)

print("\n========== RELATED MATCH ==========")
print(unified_match["related_match"])


print("\n========== LEARNING ROADMAP ==========")
print(unified_match["learning_roadmap"])