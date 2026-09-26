import re

# skills
#
# NOTE ON CATEGORIES ADDED IN THIS UPDATE
# ----------------------------------------
# The approved candidates in corrected_ontology_candidates.csv included several
# skills that did not fit cleanly into any existing category. Rather than force
# them into an unrelated bucket, the following new top-level categories were
# introduced (each holds only genuinely new, CSV-approved skills):
#   - "devops"             : CI/CD & configuration-management tooling (Ansible,
#                             Chef, Puppet, Terraform, Jenkins, GitLab CI, ...).
#                             Docker/Kubernetes were already ontology entries
#                             (in "cloud") before this update and were left
#                             there rather than moved, to avoid an unrelated
#                             structural change.
#   - "data_engineering"   : Big Data / Apache Spark - distinct from "ai_ml"
#                             (data processing/storage at scale vs modeling).
#   - "networking"         : DNS, HTTP, NTP, TCP/IP - core network protocols,
#                             not previously represented anywhere.
#   - "testing"            : QA tools/techniques (Selenium, Jasmine, Karma,
#                             PyUnit, Protractor, Regression/Exploratory Testing).
#   - "mobile_development" : Apple/iOS + hybrid mobile frameworks (Cocoa Touch,
#                             Core Animation/Data/Graphics/Text, Ionic, PhoneGap).
#   - "operating_systems"  : Linux, Windows.
#   - "cybersecurity"      : OpenAM (identity/access management). Only one
#                             entry today, but kept separate since it's a
#                             distinct domain from developer tooling.
#   - "other"              : Named products that don't fit a clean domain
#                             bucket (Mule/MuleSoft, SYSPRO ERP, WordPress),
#                             mirroring the CSV's own "Other" category label.
#
# Everything else was added into whichever existing category was the closest
# fit (e.g. ".NET"/"CSS"/"HTML"/"Bootstrap"/"jQuery" went into "web_frameworks"
# alongside the pre-existing Node.js/Tailwind CSS entries, since that category
# was already a general "web technology" bucket rather than strictly frameworks).

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
        "SQL": ["sql"],
        # --- added from approved CSV candidates ---
        "Objective-C": ["objective-c"],
        "Perl": ["perl"],
        "Scala": ["scala"],
    },
    "web_frameworks": {
        "React": ["react", "react.js", "reactjs"],
        "Next.js": ["next.js", "nextjs"],
        "Node.js": ["node.js", "nodejs"],
        "Express": ["express", "express.js"],
        "FastAPI": ["fastapi"],
        "Flask": ["flask"],
        "Django": ["django"],
        # "angular 8.x+" added as an alias per CSV instruction (not a new skill)
        "Angular": ["angular", "angular 8.x+"],
        "Vue.js": ["vue", "vue.js", "vuejs"],
        "Tailwind CSS": ["tailwind css", "tailwind"],
        # --- added from approved CSV candidates ---
        # ".NET" and ".NET Core" are kept as two separate skills per the CSV's
        # explicit instruction. See the matching-logic notes near the bottom
        # of this file for a caveat about how boundary-based substring
        # matching interacts with these two specifically.
        ".NET": [".net"],
        ".NET Core": [".net core"],
        "Bootstrap": ["bootstrap"],
        "CSS": ["css", "css3"],
        "HTML": ["html", "html5"],
        "Microsoft IIS": ["microsoft iis"],
        "jQuery": ["jquery"],
    },
    "databases": {
        "MongoDB": ["mongodb", "mongo"],
        "MySQL": ["mysql"],
        "PostgreSQL": ["postgresql", "postgres"],
        "SQLite": ["sqlite"],
        "Redis": ["redis"],
        # "oracle database" added as an alias of the existing "Oracle" entry.
        # The CSV's canonical name for this candidate was "Oracle Database",
        # but the ontology already had a working, referenced canonical name
        # "Oracle" - renaming it could break other CareerAI modules (skill
        # evidence / hierarchy / job-matching) that depend on that exact
        # string, so the existing canonical name was kept and the CSV's
        # phrasing was folded in as an alias instead.
        "Oracle": ["oracle", "oracle database"],
        # --- added from approved CSV candidates ---
        "Database Design": ["database design"],
        "Database Administration": ["database administration"],
        "Elasticsearch": ["elasticsearch"],
        "Microsoft SQL Server": ["microsoft sql server", "mssql"],
        "Relational Database Design": ["relational database design"],
    },
    "ai_ml": {
        "Machine Learning": ["machine learning", "machine-learning", "ml"],
        "Deep Learning": ["deep learning", "deep-learning", "dl"],
        "Natural Language Processing": ["natural language processing", "nlp"],
        "Computer Vision": ["computer vision"],
        "Large Language Models": [
            "large language models",
            "large language model",
            "llm",
            "llms",
        ],
        "LLM Integration": ["llm integration", "llm integrations"],
        "Prompt Engineering": ["prompt engineering"],
        "Generative AI": ["generative ai", "gen ai"],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        # --- added from approved CSV candidates ---
        # Bare "ANN" was deliberately left out of the alias list: it's a
        # common short name/initialism outside of ML contexts, so only the
        # unambiguous spelled-out forms are matched.
        "Artificial Neural Networks (ANN)": [
            "artificial neural network (ann)",
            "artificial neural networks (ann)",
        ],
        "Image Processing": ["image processing"],
        "Keras": ["keras"],
        "OpenCV": ["opencv"],
    },
    "cloud": {
        "AWS": ["aws", "amazon web services"],
        "AWS S3": ["aws s3", "amazon s3"],
        "Microsoft Azure": ["microsoft azure", "azure"],
        "Google Cloud": ["google cloud", "google cloud platform", "gcp"],
        "Docker": ["docker"],
        "Kubernetes": ["kubernetes", "k8s"],
        # --- added from approved CSV candidates ---
        # "Azure Functions" is kept distinct from "Microsoft Azure" (specific
        # serverless product vs. the platform as a whole).
        "Azure Functions": ["azure functions"],
        "Cloud Computing": ["cloud computing"],
        "Cloudify": ["cloudify"],
    },
    "developer_tools": {
        "Git": ["git"],
        "GitHub": ["github"],
        "GitLab": ["gitlab"],
        "Postman": ["postman"],
        "VS Code": ["vs code", "visual studio code"],
        "Monaco Editor": ["monaco editor", "monaco"],
        "Passport.js": ["passport.js", "passport"],
        # --- added from approved CSV candidates ---
        "Bash": ["bash"],
        "Gerrit": ["gerrit"],
        "IBM Rational ClearCase": ["ibm rational clearcase"],
        # Distinct from "Git" - the general practice/concept, not one tool.
        "Version Control": ["version control"],
    },
    "backend_concepts": {
        "REST API": [
            "rest api",
            "rest apis",
            "restful api",
            "restful apis",
            "restful services",
        ],
        "WebSockets": [
            "websocket",
            "websockets",
            "web socket",
            "web sockets",
        ],
        "Socket.IO": ["socket.io", "socket io"],
        "Authentication": ["authentication"],
        "Authorization": ["authorization"],
        "RBAC": ["rbac", "role based access control", "role-based access control"],
        "JSON": ["json"],
        "JSON Schema": ["json schema", "json-based"],
        "Pydantic": ["pydantic"],
        "API Orchestration": ["api orchestration"],
        "Secure File Handling": ["secure file handling"],
        "Protected Routes": ["protected routes"],
        # --- added from approved CSV candidates ---
        # Placed alongside REST API (same domain: API technologies), rather
        # than in "web_frameworks", for consistency with where REST API
        # already lives.
        "GraphQL": ["graphql"],
    },
    "software_engineering": {
        "Object-Oriented Programming": [
            "oop",
            "object oriented programming",
            "object-oriented programming",
        ],
        "Real-Time Systems": ["real-time", "real time"],
        "RESTful Backend": ["restful backend"],
        "Web Application Development": ["web application development"],
        "Full-Stack Development": ["full-stack", "full stack"],
        "Concurrent Systems": ["concurrent users", "concurrency"],
        # --- added from approved CSV candidates ---
        "Microservices": ["microservices", "micro-services", "micro-services pattern"],
        # Kept separate from "Object-Oriented Programming" per the
        # no-merge-distinct-technologies rule - design and programming are
        # related but not identical skills.
        "Object-Oriented Design": ["object-oriented design", "object oriented design"],
    },
    "soft_skills": {
        "Communication": ["communication"],
        "Leadership": ["leadership"],
        "Teamwork": ["teamwork", "team work"],
        "Problem Solving": ["problem solving", "problem-solving"],
    },
    # ================= NEW CATEGORIES (see note at top of file) =================
    "devops": {
        "Ansible": ["ansible"],
        "CFEngine": ["cfengine"],
        "Pipeline as Code": ["pipeline as code", "ci pipelines via code"],
        "Chef": ["chef"],
        "CI/CD": ["ci/cd"],
        "Cobbler": ["cobbler"],
        "Foreman": ["foreman"],
        "GitLab CI": ["gitlab ci"],
        "Jenkins": ["jenkins"],
        "Puppet": ["puppet"],
        "Terraform": ["terraform"],
    },
    "data_engineering": {
        "Big Data": ["big data"],
        # Bare "Spark" is deliberately excluded - the CSV flagged it as an
        # ambiguous term, so only the unambiguous "Apache Spark" form is
        # matched.
        "Apache Spark": ["apache spark"],
    },
    "networking": {
        "DNS": ["dns"],
        "HTTP": ["http"],
        "NTP": ["ntp"],
        "TCP/IP": ["tcp/ip"],
    },
    "testing": {
        "Exploratory Testing": ["exploratory testing"],
        "Jasmine": ["jasmine"],
        "Karma": ["karma"],
        "PyUnit": ["pyunit"],
        "Regression Testing": ["regression testing"],
        "Selenium": ["selenium"],
        "Protractor": ["protractor"],
    },
    "mobile_development": {
        "Cocoa Touch": ["cocoa touch"],
        "Core Animation": ["core animation"],
        "Core Data": ["core data"],
        "Core Graphics": ["core graphics"],
        "Core Text": ["core text"],
        "Ionic": ["ionic"],
        "PhoneGap": ["phonegap"],
    },
    "operating_systems": {
        "Linux": ["linux"],
        "Windows": ["windows"],
    },
    "cybersecurity": {
        "OpenAM": ["openam"],
    },
    "other": {
        "Mule (MuleSoft)": ["mule", "mulesoft"],
        "SYSPRO ERP": ["syspro", "syspro erp"],
        "WordPress": ["wordpress"],
    },
}


# normalization
def normalize_text(text):
    """
    Normalize text before skill matching.
    eg: reactJS -> reactjs
    """
    text = text.lower()

    # Normalize different dash characters
    text = text.replace("‐", "-")
    text = text.replace("–", "-")

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
            normalized_aliases = [normalize_text(alias) for alias in aliases]
            if skill in normalized_aliases:
                return canonical_name

    return skill


def skill_in_text(text, alias):
    """
    check whether a skill exists in text
    Uses word boundaries where possible to avoid incorrect matches.
    example: 'java' should match 'Java' but shouldn't match 'javascript'
    """
    pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def skill_found_in_text(text, aliases):
    text = normalize_text(text)
    for alias in aliases:
        if skill_in_text(text, alias):
            return True
    return False


def _find_alias_matches(text, aliases):
    """Return all whole-alias matches as (start, end) spans."""
    matches = []
    for alias in aliases:
        pattern = r"(?<!\w)" + re.escape(normalize_text(alias)) + r"(?!\w)"
        matches.extend((match.start(), match.end()) for match in re.finditer(pattern, text, re.IGNORECASE))
    return matches


def extract_skills_from_text(text):
    """Extract canonical skills, preferring longer matched phrases.

    If a shorter alias is wholly contained in a longer skill mention (for
    example, C inside C++ or .NET inside .NET Core), the shorter skill is
    suppressed for that occurrence. Independent mentions still count.
    """
    text = normalize_text(text)
    matches_by_skill = []

    for category, skills in SKILL_ONTOLOGY.items():
        for canonical_name, aliases in skills.items():
            spans = _find_alias_matches(text, aliases)
            if spans:
                matches_by_skill.append((category, canonical_name, spans))

    extracted_skills = {}
    for category, canonical_name, spans in matches_by_skill:
        # Keep the skill if at least one occurrence is not contained in a
        # longer matched alias. This preserves independent mentions such as
        # "C++ and C" or ".NET and .NET Core".
        has_independent_match = False
        for start, end in spans:
            shadowed = any(
                (category, canonical_name) != (other_category, other_name)
                and other_end - other_start > end - start
                and other_start <= start and end <= other_end
                for other_category, other_name, other_spans in matches_by_skill
                for other_start, other_end in other_spans
            )
            if not shadowed:
                has_independent_match = True
                break

        if has_independent_match:
            extracted_skills.setdefault(category, []).append(canonical_name)

    return extracted_skills


# Extracted skills from resume profile
def extract_skills_from_profile(profile):
    sections_to_search = [
        "skills",
        "projects",
        "experience",
        "internships",
        "research",
        "coursework",
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


# =============================================================================
# MATCHING-LOGIC NOTES
# =============================================================================
# Extraction prefers the longest matched alias when a shorter skill alias is
# fully contained within it. This prevents C++ from also producing C, C# from
# producing C, .NET Core from producing .NET, and Relational Database Design
# from producing Database Design. A separate, independent mention of the
# shorter skill is retained (for example, "C++ and C").
# =============================================================================


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
        "rbac",
    ]

    normalized = normalize_text(test_text)
    for skill in test_skills:
        print(skill, "=>", skill_in_text(normalized, skill))

    print("\n========== FULL EXTRACTION ==========\n")
    result = extract_skills_from_text(test_text)
    print(result)
