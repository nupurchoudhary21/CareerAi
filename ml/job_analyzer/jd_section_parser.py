SECTION_ALIASES = {

    "required": [

        "requirements",
        "required skills",
        "required qualifications",
        "qualifications",
        "required",
        "must have",
        "must-have",
        "technical requirements",
        "technical qualifications",
        "minimum qualifications",
        "skills required",
        "required experience",
        "other requirements",
        "candidate requirements",
        "candidate qualifications",
        "what you need",
        "what we're looking for",
        "what we are looking for",
        "who we're looking for",
        "who we are looking for"
    ],


    "preferred": [

        "preferred skills",
        "preferred qualifications",
        "preferred",
        "nice to have",
        "nice-to-have",
        "bonus skills",
        "additional qualifications",
        "additional skills",
        "advantages",
        "preferred experience",
        "desired skills",
        "desired qualifications",
        "good to have"
    ],


    "responsibilities": [

        "responsibilities",
        "job responsibilities",
        "role responsibilities",
        "main responsibilities",
        "responsibility",
        "responsibilities and duties",
        "duties",
        "job duties",
        "duties and responsibilities",
        "what you'll do",
        "what you will do",
        "what you’ll do",
        "your responsibilities",
        "your role",
        "role",
        "job description"
    ],


    "ignore": [

        "benefits",
        "schedule",
        "supplemental pay",
        "housing rent subsidy",
        "industry",
        "work remotely",
        "work location",
        "job type",
        "compensation",
        "salary",
        "educational qualifications",
        "job location",
        "location",
        "about the company",
        "company overview",
        "about us"
    ]
}

import re


def normalize_heading(line):

    line = line.strip().lower()

    # Replace common separators
    line = line.replace("–", "-")
    line = line.replace("—", "-")

    # Remove bullets
    line = line.replace("•", "")
    line = line.replace("·", "")

    # Remove trailing punctuation
    line = re.sub(r"[:\-]+$", "", line)

    # Normalize whitespace
    line = " ".join(line.split())

    return line

def identify_section(line):

    normalized_line = normalize_heading(line)

    for section, aliases in SECTION_ALIASES.items():

        normalized_aliases = [
            normalize_heading(alias)
            for alias in aliases
        ]

        if normalized_line in normalized_aliases:
            return section

    return None

def parse_job_description(text):

    sections = {
        "required": [],
        "preferred": [],
        "responsibilities": []
    }

    current_section = None
    detected_sections = False

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        section = identify_section(line)

        if section:

            if section == "ignore":
                current_section = None

            else:
                current_section = section
                detected_sections = True

            continue

        if current_section:

            sections[current_section].append(line)

        else:

            sections["required"].append(line)

    return sections