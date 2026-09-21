from .skill_matcher import match_skills
from .match_score import calculate_match_score
from .skill_gap import build_skill_gap
from .evidence_matcher import build_evidence_aware_match
from .hierarchy_matcher import analyze_skill_relationship
from .related_skill_matcher import analyze_related_skill_match
from .learning_roadmap import generate_learning_roadmap

def build_unified_match(
    resume_skills,
    resume_skill_profile,
    jd_profile,
    skill_hierarchy
):

    # 1. Exact skill matching
    skill_match = match_skills(
        resume_skills,
        jd_profile
    )

    # 2. Match score
    match_score = calculate_match_score(
        skill_match
    )

    # 3. Evidence-aware matching
    evidence_match = build_evidence_aware_match(
        resume_skill_profile,
        jd_profile
    )

    # 4. Initialize hierarchy matching
    hierarchy_match = {
        "required": {},
        "preferred": {}
    }

    # 5. Initialize related skill matching
    related_match = {
        "required": {},
        "preferred": {}
    }

    # 6. Analyze required skills
    for skill in jd_profile["required"]["skills"]:

        hierarchy_match["required"][skill] = (
            analyze_skill_relationship(
                skill,
                resume_skills,
                skill_hierarchy
            )
        )

        related_match["required"][skill] = (
            analyze_related_skill_match(
                skill,
                resume_skills
            )
        )

    # 7. Analyze preferred skills
    for skill in jd_profile["preferred"]["skills"]:

        hierarchy_match["preferred"][skill] = (
            analyze_skill_relationship(
                skill,
                resume_skills,
                skill_hierarchy
            )
        )

        related_match["preferred"][skill] = (
            analyze_related_skill_match(
                skill,
                resume_skills
            )
        )

    # 8. Build relationship-aware skill gap
    skill_gap = build_skill_gap(
        skill_match,
        related_match
    )

    learning_roadmap = generate_learning_roadmap(
        skill_gap["critical_gaps"],
        resume_skills
    )

    # 9. Final unified result
    return {
        "match_score": match_score,
        "skill_match": skill_match,
        "skill_gap": skill_gap,
        "evidence_match": evidence_match,
        "hierarchy_match": hierarchy_match,
        "related_match": related_match,
        "learning_roadmap": learning_roadmap
    }