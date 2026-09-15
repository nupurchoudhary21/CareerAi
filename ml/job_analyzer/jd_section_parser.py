SECTION_ALIASES = {
    "required" : [
        "requirements",
        "required skills",
        "required qualifications",
        "qualification",
        "must have",
        "must-have",
        "technical requirements",
        "minimum qualifications"
    ],

    "preferred": [
        "preferred skills",
        "preferred qualifications",
        "nice to have",
        "nice-to-have",
        "preferred",
        "bonus skills",
        "additional qualifiactions"
    ],

    "responsibilites": [
        "responsibilities",
        "what you'll do",
        "what you will do",
        "job responsibilities",
        "role responsibilities"
    ]
}

def normalize_heading(line):
    line = line.strip().lower()

    line = line.replace("-","-")
    line = line.replace("—", "-")
    line = line.replace(":", "")
    line = line.replace("•", "")

    line = " ".join(line.split())

    return line


def identify_section(line):
    line = normalize_heading(line)

    for section, aliases in SECTION_ALIASES.items():
        normalize_aliases = [
            normalize_heading(alias)
            for alias in aliases
        ]

        if line in normalize_aliases:
            return section

    return None

def parse_job_description(text):
    sections = {
        "required": [],
        "preferred": [],
        "responsibilities": []
    }

    current_section = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        section = identify_section(line)

        if section:
            current_section = section
            continue

        if current_section in sections:
         sections[current_section].append(line)

    return sections          