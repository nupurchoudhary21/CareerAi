from .skill_matcher import match_skills
from .match_score import calculate_match_score
from .skill_gap import build_skill_gap
from .evidence_matcher import build_evidence_aware_match
from .hierarchy_matcher import analyze_skill_relationship

def build_unified_match(
        resume_skills,
        resume_skill_profile,
        jd_profile,
        skill_hierarchy
):
    # direct skill matching

    skill_match = match_skills(

        resume_skills,
        jd_profile
    )

    # calculate match score
    match_score = calculate_match_score(
        skill_match
    )

    # build skill gap
    skill_gap = build_skill_gap(
        skill_match
    )

    # evidence aware matching 
    evidence_match = build_evidence_aware_match(
        resume_skill_profile,
        jd_profile
    )

    # Hierarchy-aware matching
    hierarchy_match = {
        "required": {},
        "preferred": {}
    }

    for skill in jd_profile["required"]["skills"]:
        hierarchy_match["required"][skill] = analyze_skill_relationship(
            skill,
            resume_skills,
            skill_hierarchy
        )

    for skill in jd_profile["preferred"]["skills"]:
        hierarchy_match["preferred"][skill] = analyze_skill_relationship(
            skill,
            resume_skills,
            skill_hierarchy
        )

    return {
        "match_score": match_score,
        "skill_match": skill_match,
        "skill_gap": skill_gap,
        "evidence_match": evidence_match,
        "hierarchy_match": hierarchy_match
    }
