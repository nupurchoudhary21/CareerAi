# ml/job_analyzer/candidate_classifier.py

CONFIRMED_SKILLS = {
    "python",
    "java",
    "javascript",
    "c++",
    "c#",
    "go",
    "ruby",
    "scala",
    "perl",
    "react",
    "angular",
    "vue",
    "node.js",
    "django",
    "docker",
    "kubernetes",
    "tensorflow",
    "pytorch",
    "keras",
    "mongodb",
    "mysql",
    "postgresql",
    "redis",
    "git",
    "jenkins",
    "terraform",
    "ansible",
    "linux",
    "graphql",
    "opencv",
    "spark",
    "elasticsearch",
}

JOB_RESPONSIBILITIES = {
    "database programmer",
    "security specialist",
    "software engineer",
    "software technician",
    "training development specialist",
    "multimedia program develop",
}

POSSIBLE_SKILLS = {
    "big data",
    "applied mathematics",
    "fraud prevention",
    "metadata",
    "telecommunication",
    "version control",
    "database documentation",
    "defect management",
    "test management",
    "standard procedure definition",
}


def classify_candidate(candidate):
    """
    Classify a candidate as a confirmed skill,
    possible skill, or job responsibility.
    """

    normalized = candidate.strip().lower()

    if normalized in CONFIRMED_SKILLS:
        return "confirmed_skill"

    if normalized in JOB_RESPONSIBILITIES:
        return "job_responsibility"

    if normalized in POSSIBLE_SKILLS:
        return "possible_skill"

    return "possible_skill"
