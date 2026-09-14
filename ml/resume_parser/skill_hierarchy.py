# Parent-child relationships between skills

SKILL_HIERARCHY = {

    # Cloud
    "AWS S3": {
        "parent": "AWS"
    },

    # JavaScript ecosystem
    "React": {
        "parent": "JavaScript"
    },

    "Next.js": {
        "parent": "JavaScript"
    },

    "Node.js": {
        "parent": "JavaScript"
    },

    # WebSocket ecosystem
    "Socket.IO": {
        "parent": "WebSockets"
    }

}

def get_parent_skill(skill):
    """
    return the parent skill if one exists.
    """

    relationship = SKILL_HIERARCHY.get(skill)

    if relationship:
        return relationship.get("parent")


    return None


def get_child_skills(skill):
    """
    Return all direct child skills.
    """

    children = []

    for child, relationship in SKILL_HIERARCHY.items():

        if relationship.get("parent") == skill:
            children.append(child)

    return children


def get_skill_relationship(skill):
    """
    Return parent and child relationships for a skill.
    """

    return {
        "skill": skill,
        "parent": get_parent_skill(skill),
        "children": get_child_skills(skill)
    }



def deduplicate_skills(skills):
    """
    Remove duplicate skills while preserving order.
    """

    unique_skills = []

    for skill in skills:

        if skill not in unique_skills:
            unique_skills.append(skill)

    return unique_skills


def build_skill_hierarchy(skill_list):

    hierarchy = {}

    for skill in skill_list:

        hierarchy[skill] = {
            "parent": get_parent_skill(skill),
            "children": get_child_skills(skill)
        }

    return hierarchy