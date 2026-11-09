# from resume_parser.skill_extractor import skill_evidence

from .skill_matcher import match_skills
from .match_score import calculate_match_score
from .skill_gap import build_skill_gap
from .evidence_matcher import build_evidence_aware_match
from .hierarchy_matcher import analyze_skill_relationship
from .related_skill_matcher import analyze_related_skill_match
from .learning_roadmap import generate_learning_roadmap
# from ml.job_analyzer import skill_gap

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

    skill_evidence = build_roadmap_evidence(resume_skill_profile)

    print("\n========== ROADMAP EVIDENCE DEBUG ==========")

    for skill, confidence in skill_evidence.items():
        print(f"{skill}: {confidence}")

    learning_roadmap = generate_learning_roadmap(
        skill_gap["critical_gaps"],
        resume_skills,
        skill_evidence=skill_evidence
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


def build_roadmap_evidence(resume_skill_profile):
    skill_evidence = {}

    confidence_mapping = {
        "high": 1.0,
        "medium": 0.6,
        "low": 0.3
    }

    for skill, skill_data in resume_skill_profile.items():

        evidence = skill_data.get("evidence", {})

        confidence = evidence.get("confidence", "low")

        if isinstance(confidence, str):
            confidence = confidence_mapping.get(
                confidence.lower(), 0.0
            )

        elif not isinstance(confidence, (int, float)):
            confidence = 0.0

        skill_evidence[skill] = float(confidence)

    return skill_evidence
