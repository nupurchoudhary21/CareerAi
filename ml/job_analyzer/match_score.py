def calculate_match_score(skill_match):

    matched_required = skill_match["matched_required"]
    missing_required = skill_match["missing_required"]

    matched_preferred  = skill_match["matched_preferred"]
    missing_preferred = skill_match["missing_preferred"]

    total_required = len(matched_required) + len(missing_required)
    total_preferred = len(matched_preferred) + len(missing_preferred)

    if total_required > 0:
        required_score =(
            len(matched_required)/ total_required
        ) * 70

    else:
        required_score = 0

    if total_preferred > 0:
        preferred_score = (
            len(matched_preferred)/ total_preferred
        ) * 30

    else:
        preferred_score = 0

    final_score = required_score + preferred_score

    return{
        "required_score": round(required_score,2),
        "preferred_score": round(preferred_score,2),
        "matched_score": round(final_score,2)

    }               