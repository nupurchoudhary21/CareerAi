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

    results.sort(
        key=lambda x: x["skill_count"]
    )

for result in results[:10]:

    print("\n" + "=" * 80)

    print(
        f"TITLE: {result['job_title']}"
    )

    print(
        f"SKILLS FOUND: {result['skill_count']}"
    )

    print(
        f"CURRENT SKILLS: {result['skills']}"
    )

    print("\nJOB DESCRIPTION:\n")

    print(result["job_description"])

    print("=" * 80)