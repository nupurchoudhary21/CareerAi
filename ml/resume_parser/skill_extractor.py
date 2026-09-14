import re

# skills

SKILL_ONTOLOGY = {

    "programming_languages": {
        "Python": ["python"],
        "Java": ["java"],
        "C": ["c"],
        "C++": ["c++", "cpp"],
        "C#": ["c#", "csharp"],
        "JavaScript": ["javascript", "js"],
        "TypeScript": ["typescript", "ts"],
        "Go": ["golang"],
        "Rust": ["rust"],
        "PHP": ["php"],
        "Ruby": ["ruby"],
        "Kotlin": ["kotlin"],
        "Swift": ["swift"],
        "SQL": ["sql"]
    },

    "web_frameworks": {
        "React": ["react", "react.js", "reactjs"],
        "Next.js": ["next.js", "nextjs"],
        "Node.js": ["node.js", "nodejs"],
        "Express": ["express", "express.js"],
        "FastAPI": ["fastapi"],
        "Flask": ["flask"],
        "Django": ["django"],
        "Angular": ["angular"],
        "Vue.js": ["vue", "vue.js", "vuejs"],
        "Tailwind CSS": ["tailwind css", "tailwind"]
    },

    "databases": {
        "MongoDB": ["mongodb", "mongo"],
        "MySQL": ["mysql"],
        "PostgreSQL": ["postgresql", "postgres"],
        "SQLite": ["sqlite"],
        "Redis": ["redis"],
        "Oracle": ["oracle"]
    },

    "ai_ml": {
        "Machine Learning": [
            "machine learning",
            "machine-learning",
            "ml"
        ],
        "Deep Learning": [
            "deep learning",
            "deep-learning",
            "dl"
        ],
        "Natural Language Processing": [
            "natural language processing",
            "nlp"
        ],
        "Computer Vision": [
            "computer vision"
        ],
        "Large Language Models": [
            "large language models",
            "large language model",
            "llm",
            "llms"
        ],
        "LLM Integration": [
            "llm integration",
            "llm integrations"
        ],
        "Prompt Engineering": [
            "prompt engineering"
        ],
        "Generative AI": [
            "generative ai",
            "gen ai"
        ],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "Scikit-learn": [
            "scikit-learn",
            "sklearn"
        ],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"]
    },

    "cloud": {
        "AWS": [
            "aws",
            "amazon web services"
        ],
        "AWS S3": [
            "aws s3",
            "amazon s3"
        ],
        "Microsoft Azure": [
            "microsoft azure",
            "azure"
        ],
        "Google Cloud": [
            "google cloud",
            "google cloud platform",
            "gcp"
        ],
        "Docker": ["docker"],
        "Kubernetes": [
            "kubernetes",
            "k8s"
        ]
    },

    "developer_tools": {
        "Git": ["git"],
        "GitHub": ["github"],
        "GitLab": ["gitlab"],
        "Postman": ["postman"],
        "VS Code": [
            "vs code",
            "visual studio code"
        ],
        "Monaco Editor": [
            "monaco editor",
            "monaco"
        ],
        "Passport.js": [
            "passport.js",
            "passport"
        ]
    },

    "backend_concepts": {
        "REST API": [
            "rest api",
            "rest apis",
            "restful api",
            "restful apis"
        ],
        "WebSockets": [
            "websocket",
            "websockets",
            "web socket",
            "web sockets"
        ],
        "Socket.IO": [
            "socket.io",
            "socket io"
        ],
        "Authentication": [
            "authentication"
        ],
        "Authorization": [
            "authorization"
        ],
        "RBAC": [
            "rbac",
            "role based access control",
            "role-based access control"
        ],
        "JSON": [
            "json"
        ],
        "JSON Schema": [
            "json schema",
            "json-based"
        ],
        "Pydantic": [
            "pydantic"
        ],
        "API Orchestration": [
            "api orchestration"
        ],
        "Secure File Handling": [
            "secure file handling"
        ],
        "Protected Routes": [
            "protected routes"
        ]
    },

    "software_engineering": {
        "Object-Oriented Programming": [
            "oop",
            "object oriented programming",
            "object-oriented programming"
        ],
        "Real-Time Systems": [
            "real-time",
            "real time"
        ],
        "RESTful Backend": [
            "restful backend"
        ],
        "Web Application Development": [
            "web application development"
        ],
        "Full-Stack Development": [
            "full-stack",
            "full stack"
        ],
        "Concurrent Systems": [
            "concurrent users",
            "concurrency"
        ]
    },

    "soft_skills": {
        "Communication": [
            "communication"
        ],
        "Leadership": [
            "leadership"
        ],
        "Teamwork": [
            "teamwork",
            "team work"
        ],
        "Problem Solving": [
            "problem solving",
            "problem-solving"
        ]
    }
}

# normalization 

def normalize_text(text):
    """

    Normalize text before skill matching.
    eg: reactJS -> reactjs
    
    """

    text = text.lower()

    # Normalize different dash characters
    text = text.replace("-","-")
    text = text.replace("-","-")

    # remove unnecessary whitespaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_skill(skill):
    """
    convert a detected skill/alias into its canonical name
    """    

    skill = normalize_text(skill)

    for category, skills in SKILL_ONTOLOGY.items():

        for canonical_name, aliases in skills.items():

            normalized_aliases = [
                normalize_text(alias)
                for alias in aliases
            ]

            if skill in normalized_aliases:
                return canonical_name

        return skill


def skill_in_text(text, alias):
    """
    check whether a skill exists in text
    Uses word boundaries where possible to avoid incorrect matches.

    example:
    'java' should match 'Java'
    but shouldn't match 'javascript' 
    
    """        

    pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

    return re.search(
        pattern,
        text,
        re.IGNORECASE
    ) is not None


def skill_found_in_text(text, aliases):
    text = normalize_text(text)

    for alias in aliases:
        if skill_in_text(text, alias):
            return True

    return False    


def extract_skills_from_text(text):

    text = normalize_text(text)

    extracted_skills = {}

    for category in SKILL_ONTOLOGY:

        detected = []

        skills = SKILL_ONTOLOGY[category]

        for canonical_name in skills:

            aliases = skills[canonical_name]

            for alias in aliases:

                if skill_in_text(text, alias):

                    detected.append(canonical_name)

                    break

        if detected:
            extracted_skills[category] = detected

    return extracted_skills


# Extracted skills from resume profile
                    
def extract_skills_from_profile(profile):

    sections_to_search = [
        "skills",
        "projects",
        "experience",
        "internships",
        "research",
        "coursework"
    ]

    text_parts = []

    for section in sections_to_search:

        section_data = profile.get(section, [])

        if isinstance(section_data, list):
            text_parts.extend(section_data)

        elif isinstance(section_data, str):
            text_parts.append(section_data)

    combined_text = " ".join(text_parts)

    return extract_skills_from_text(combined_text)



# flatten skills

def get_all_skills(skill_profile):

    """
    convert categorized skills into one flat list
    """

    all_skills = []

    for skills in skill_profile.values():
        for skill in skills:
            if skill not in all_skills:
                all_skills.append(skill)

    return all_skills        



if __name__ == "__main__":

    test_text = """
    Python, C, C++, Java, JavaScript, SQL
    Next.js, React.js, Node.js, Express, FastAPI, Flask, Tailwind CSS
    MongoDB, SQL, AWS S3
    REST APIs, LLM Integration, Prompt Engineering, Pydantic, JSON Schema Design
    OOP, Authentication, Authorization, RBAC, WebSockets, Secure File Handling
    Git, GitHub, Socket.IO, Postman
    """

    print("\n========== TESTING INDIVIDUAL SKILLS ==========\n")

    test_skills = [
        "python",
        "react.js",
        "node.js",
        "mongodb",
        "aws s3",
        "fastapi",
        "github",
        "socket.io",
        "websockets",
        "rbac"
    ]

    normalized = normalize_text(test_text)

    for skill in test_skills:

        print(
            skill,
            "=>",
            skill_in_text(normalized, skill)
        )

    print("\n========== FULL EXTRACTION ==========\n")

    result = extract_skills_from_text(test_text)

    print(result)