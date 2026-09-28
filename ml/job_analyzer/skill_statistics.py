from .job_loader import load_jobs
from .jd_cleaner import clean_job_description
from .jd_section_parser import parse_job_description
from .jd_skill_extractor import extract_skills_from_jd


def analyze_skill_coverage(jobs):

    results = []

    for index, job in enumerate(jobs):

        job_description = clean_job_description(
            job["job_description"]
        )

        sections = parse_job_description(
            job_description
        )

        extracted_skills = extract_skills_from_jd(
            sections
        )

        job_skills = set()

        for section_skills in extracted_skills.values():

            for skill in section_skills:
                job_skills.add(skill)

        results.append({
            "job_index": index,
            "job_title": job["job_title"],
            "skill_count": len(job_skills),
            "skills": sorted(job_skills),
            "job_description": job_description
        })

    return results

if __name__ == "__main__":

    jobs = load_jobs(
        "../datasets/jobs/jobs.csv"
    )

    results = analyze_skill_coverage(jobs)

    # Count how often each skill appears
    skill_frequency = {}

    for result in results:
        for skill in result["skills"]:
            skill_frequency[skill] = (
                skill_frequency.get(skill, 0) + 1
            )

    # Sort skills by frequency
    sorted_skills = sorted(
        skill_frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print(f"\nTotal jobs analyzed: {len(results)}")
    print(f"Unique skills found: {len(skill_frequency)}")

    print("\nTOP 50 MOST FREQUENT SKILLS")
    print("=" * 60)

    for skill, count in sorted_skills[:50]:
        percentage = (count / len(results)) * 100

        print(
            f"{skill:<30} "
            f"{count:>5} jobs "
            f"({percentage:.2f}%)"
        )

    print("\nJOBS WITH THE FEWEST EXTRACTED SKILLS")
    print("=" * 60)

    results.sort(key=lambda x: x["skill_count"])

    for result in results[:10]:
        print(
            f"{result['job_title']}: "
            f"{result['skill_count']} skills"
        )

    print("\nZERO-SKILL JOB DESCRIPTIONS")
    print("=" * 80)

    zero_skill_jobs = [
        result for result in results
        if result["skill_count"] == 0
    ]

    for result in zero_skill_jobs[:10]:
        print(f"\nTITLE: {result['job_title']}")
        print("\nDESCRIPTION:")
        print(result["job_description"])
        print("=" * 80)    