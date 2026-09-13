SECTION_ALIASES = {

    # -------------------------
    # PERSONAL INFORMATION
    # -------------------------

    "contact": [
        "contact",
        "contact information",
        "contact details",
        "personal information",
        "personal details"
    ],

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "professional profile",
        "career summary",
        "career profile",
        "about me",
        "objective",
        "career objective",
        "professional objective"
    ],

    # -------------------------
    # EDUCATION
    # -------------------------

    "education": [
        "education",
        "educational background",
        "academic background",
        "academic qualifications",
        "academic history",
        "educational qualifications",
        "academic profile",
        "qualifications"
    ],

    "coursework": [
        "coursework",
        "relevant coursework",
        "academic coursework",
        "courses",
        "relevant courses",
        "subjects",
        "coursework and skills",
        "coursework skills"
    ],

    # -------------------------
    # SKILLS
    # -------------------------

    "skills": [
        "skills",
        "technical skills",
        "technical expertise",
        "technical competencies",
        "core competencies",
        "core skills",
        "key skills",
        "professional skills",
        "areas of expertise",
        "expertise",
        "competencies",
        "technologies",
        "tools and technologies",
        "technical proficiencies",
        "technical knowledge",
        "skills and technologies",
        "technical skill set",
        "technical skillset",
        "technical abilities",
        "technical knowledge and skills"
    ],

    # -------------------------
    # EXPERIENCE
    # -------------------------

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "career history",
        "professional history",
        "relevant experience",
        "industry experience"
    ],

    "internships": [
        "internships",
        "internship experience",
        "internship",
        "summer internship",
        "industrial training",
        "training experience"
    ],

    "research_experience": [
        "research experience",
        "research",
        "research work",
        "research projects",
        "academic research",
        "research background"
    ],

    # -------------------------
    # PROJECTS
    # -------------------------

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
        "major projects",
        "technical projects",
        "software projects",
        "selected projects",
        "relevant projects",
        "project experience",
        "academic project",
        "personal project"
    ],

    # -------------------------
    # CERTIFICATIONS
    # -------------------------

    "certifications": [
        "certifications",
        "certificates",
        "professional certifications",
        "technical certifications",
        "certification",
        "licenses",
        "licenses and certifications",
        "certifications and training"
    ],

    # -------------------------
    # ACHIEVEMENTS
    # -------------------------

    "achievements": [
        "achievements",
        "accomplishments",
        "honors",
        "honours",
        "academic achievements",
        "professional achievements",
        "key achievements",
        "notable achievements"
    ],

    # -------------------------
    # AWARDS
    # -------------------------

    "awards": [
        "awards",
        "awards and honors",
        "awards & honors",
        "honors and awards",
        "honours and awards",
        "recognition",
        "recognitions"
    ],

    # -------------------------
    # PUBLICATIONS
    # -------------------------

    "publications": [
        "publications",
        "research publications",
        "academic publications",
        "papers",
        "research papers",
        "published papers",
        "journal publications",
        "conference publications"
    ],

    # -------------------------
    # LEADERSHIP
    # -------------------------

    "leadership": [
        "leadership",
        "leadership experience",
        "leadership roles",
        "leadership activities",
        "team leadership"
    ],

    # -------------------------
    # POSITIONS OF RESPONSIBILITY
    # -------------------------

    "responsibilities": [
        "positions of responsibility",
        "position of responsibility",
        "positions of responsibilities",
        "responsibilities",
        "roles and responsibilities",
        "leadership and responsibility"
    ],

    # -------------------------
    # VOLUNTEERING
    # -------------------------

    "volunteering": [
        "volunteer experience",
        "volunteering",
        "volunteer work",
        "community service",
        "social work",
        "community involvement"
    ],

    # -------------------------
    # EXTRACURRICULAR
    # -------------------------

    "extracurricular": [
        "extracurricular activities",
        "extracurricular",
        "co-curricular activities",
        "activities",
        "student activities",
        "campus activities"
    ],

    # -------------------------
    # LANGUAGES
    # -------------------------

    "languages": [
        "languages",
        "language skills",
        "spoken languages",
        "linguistic skills"
    ],

    # -------------------------
    # INTERESTS
    # -------------------------

    "interests": [
        "interests",
        "areas of interest",
        "professional interests",
        "personal interests",
        "hobbies",
        "hobbies and interests"
    ],

    # -------------------------
    # COMMUNITY
    # -------------------------

    "community": [
        "community involvement",
        "community service",
        "social activities",
        "social involvement"
    ],

    # -------------------------
    # REFERENCES
    # -------------------------

    "references": [
        "references",
        "professional references",
        "references available upon request"
    ]
}


def normalize_heading(line):

    line = line.strip().lower()

    # Normalize common PDF characters
    line = line.replace("–", "-")
    line = line.replace("—", "-")

    # Normalize &
    line = line.replace("&", "and")

    # Remove common punctuation
    line = line.replace(":", "")
    line = line.replace("•", "")
    line = line.replace("|", "")

    # Remove extra spaces
    line = " ".join(line.split())

    return line


def identify_section(line):

    line = normalize_heading(line)


    for section, aliases in SECTION_ALIASES.items():

        normalized_aliases = [
            normalize_heading(alias)
            for alias in aliases
        ]

        if line in normalized_aliases:
            return section

    return None


def parse_sections(text):

    sections = {}
    current_section = None

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        detected_section = identify_section(line)

        if detected_section:

            current_section = detected_section

            if current_section not in sections:
                sections[current_section] = []

            # Don't add heading itself as content
            continue

        if current_section:
            sections[current_section].append(line)

    return sections


def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:
        return lines[0]

    return None


def create_resume_profile(sections, name):

    profile = {

        "personal": {
            "name": name
        },

        "summary": sections.get("summary", []),

        "education": sections.get("education", []),

        "coursework": sections.get("coursework", []),

        "skills": sections.get("skills", []),

        "experience": sections.get("experience", []),

        "internships": sections.get("internships", []),

        "research": sections.get("research_experience", []),

        "projects": sections.get("projects", []),

        "certifications": sections.get("certifications", []),

        "achievements": sections.get("achievements", []),

        "awards": sections.get("awards", []),

        "publications": sections.get("publications", []),

        "leadership": sections.get("leadership", []),

        "volunteering": sections.get("volunteering", []),

        "extracurricular": sections.get("extracurricular", []),

        "languages": sections.get("languages", []),

        "interests": sections.get("interests", [])

    }

    return profile