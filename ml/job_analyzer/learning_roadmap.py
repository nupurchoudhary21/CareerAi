SKILL_PREREQUISITES = {

    "Django": [
        "Python",
        "SQL",
        "HTTP",
        "REST API"
    ],

    "FastAPI": [
        "Python",
        "HTTP",
        "REST API"
    ],

    "React": [
        "JavaScript",
        "HTML/CSS"
    ],

    "Next.js": [
        "JavaScript",
        "React"
    ]
}

SKILL_LEARNING_PATHS = {

    "Django": [
        "Django fundamentals",
        "Django project structure",
        "URLs and views",
        "Templates",
        "Models and ORM",
        "Forms",
        "Authentication",
        "Django REST Framework",
        "Testing",
        "Build a Django REST API"
    ],

    "FastAPI": [
        "FastAPI fundamentals",
        "Routing",
        "Request and response handling",
        "Pydantic models",
        "Dependency injection",
        "Authentication",
        "Database integration",
        "Testing",
        "Build a FastAPI project"
    ],

    "React": [
        "React fundamentals",
        "Components",
        "Props and state",
        "Event handling",
        "Hooks",
        "Forms",
        "API integration",
        "Routing",
        "State management",
        "Build a React application"
    ]
}

LEARNING_TOPIC_SKILLS = {

    "Django fundamentals": [
        "Django"
    ],

    "Django project structure": [
        "Django"
    ],

    "URLs and views": [
        "Django"
    ],

    "Templates": [
        "Django"
    ],

    "Models and ORM": [
        "Django",
        "SQL"
    ],

    "Forms": [
        "Django"
    ],

    "Authentication": [
        "Django",
        "Authentication"
    ],

    "Django REST Framework": [
        "Django",
        "REST API"
    ],

    "Testing": [
        "Django"
    ],

    "Build a Django REST API": [
        "Django",
        "REST API"
    ]
}

LEARNING_TOPIC_STAGES = {

    "Django fundamentals": "Foundation",

    "Django project structure": "Foundation",

    "URLs and views": "Core Development",

    "Templates": "Core Development",

    "Models and ORM": "Core Development",

    "Forms": "Core Development",

    "Authentication": "Advanced",

    "Django REST Framework": "Advanced",

    "Testing": "Testing",

    "Build a Django REST API": "Project"
}

SKILL_PRACTICE_PROJECTS = {

    "Django": [
        "Build a Django REST API",
        "Build a Django authentication system"
    ],

    "FastAPI": [
        "Build a FastAPI backend with database integration"
    ],

    "React": [
        "Build a React application consuming a REST API"
    ],

    "Next.js": [
        "Build a full-stack Next.js application"
    ]
}



def generate_learning_roadmap(
    missing_skills,
    resume_skills
):
    roadmap = {}

    for skill in missing_skills:

        prerequisites = SKILL_PREREQUISITES.get(
            skill,
            []
        )

        learning_path = SKILL_LEARNING_PATHS.get(
            skill,
            []
        )

        known_prerequisites = []
        missing_prerequisites = []

        # Check prerequisites
        for prerequisite in prerequisites:

            if prerequisite in resume_skills:
                known_prerequisites.append(
                    prerequisite
                )
            else:
                missing_prerequisites.append(
                    prerequisite
                )

        # Build personalized learning path
        staged_path = {}

        for topic in learning_path:

            required_skills = LEARNING_TOPIC_SKILLS.get(
                topic,
                []
            )

            already_known = False

            for required_skill in required_skills:

                if required_skill in resume_skills:
                    already_known = True
                    break

            if not already_known:

                stage = LEARNING_TOPIC_STAGES.get(
                    topic,
                    "General"
                )

                if stage not in staged_path:
                    staged_path[stage] = []

                staged_path[stage].append(topic)

        practice_projects = SKILL_PRACTICE_PROJECTS.get(
            skill,
            []
        )

        roadmap[skill] = {
            "known_prerequisites": known_prerequisites,
            "missing_prerequisites": missing_prerequisites,
            "learning_path": staged_path,
            "practice_projects": practice_projects
        }

    return roadmap   


# testing of the file 

# if __name__ == "__main__":

#     missing_skills = ["Django"]

#     resume_skills = [
#         "Python",
#         "SQL",
#         "REST API",
#         "Flask"
#     ]

#     roadmap = generate_learning_roadmap(
#         missing_skills,
#         resume_skills
#     )

#     print("\nLEARNING ROADMAP:")
#     print(roadmap)           

if __name__ == "__main__":

    missing_skills = ["Django"]

    resume_skills = [
        "Python",
        "SQL",
        "REST API",
        "Flask",
        "Authentication"
    ]

    roadmap = generate_learning_roadmap(
        missing_skills,
        resume_skills
    )

    print("\nLEARNING ROADMAP:")
    print(roadmap)