from resume_parser.pdf_parser import extract_text_from_pdf
from resume_parser.text_cleaner import clean_text

from resume_parser.section_parser import (
    parse_sections,
    create_resume_profile,
    extract_name
)


pdf_path = "../datasets/resumes/resume2.pdf"

raw_text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(raw_text)

name = extract_name(cleaned_text)

sections = parse_sections(cleaned_text)

profile = create_resume_profile(sections, name)

print("\n========== RESUME PROFILE ==========\n")
print(profile)