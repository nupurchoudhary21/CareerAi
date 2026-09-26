import re

from ..resume_parser.skill_extractor import SKILL_ONTOLOGY

def normalize_text(text):

    """
    Normalize text for comparison.
    """
    text = text.lower().strip()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"\s+", " ", text)

    return text

def build_skill_alias_map():
    """
    Build: 
         normalized alias -> canonical skill

    from the existing SKILL_ONTOLOGY     
    """

    alias_map = {}

    for category, skills in SKILL_ONTOLOGY.items():
        for canonical_name, aliases in skills.items():

            alias_map[normalize_text(canonical_name)] = canonical_name

            for alias in aliases:
                alias_map[
                    normalize_text(alias)
                ] = canonical_name

    return alias_map

def normalize_skill(candidate, alias_map):
    """
    Map one LLM candidate to a canonical ontology skill.

    Returns:
        {
            "candidate": original candidate,
            "normalized": canonical skill or None,
            "known": True/False
        }
    """

    normalized_candidate = normalize_text(candidate)

    if normalized_candidate in alias_map:

        return {
            "candidate": candidate,
            "normalized": alias_map[normalized_candidate],
            "known": True
        }

    return {
        "candidate": candidate,
        "normalized": None,
        "known": False
    }


def normalize_candidates(candidates):
    """
    Normalize a list of LLM-generated skill candidates.
    """

    alias_map = build_skill_alias_map()

    results = []

    for candidate in candidates:

        result = normalize_skill(
            candidate,
            alias_map
        )

        results.append(result)

    return results


if __name__ == "__main__":

    test_candidates = [
        "Python",
        "Python Programming",
        "React.js",
        "ReactJS",
        "CISCO",
        "CCNA",
        "Flutter",
        "WordPress"
    ]

    results = normalize_candidates(
        test_candidates
    )

    print("\nNORMALIZATION RESULTS:\n")

    for result in results:

        print(
            f"{result['candidate']} "
            f"-> {result['normalized']} "
            f"(known={result['known']})"
        )


