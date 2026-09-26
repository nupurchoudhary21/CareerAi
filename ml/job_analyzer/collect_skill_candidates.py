from .job_loader import load_jobs
from .skill_candidate_extractor import extract_skill_candidates
from .skill_normalizer import normalize_candidates

jobs = load_jobs("datasets/jobs/jobs.csv")

all_candidates = []

for i, job in enumerate(jobs, start=1):

    print(f"\nProcessing job {i}...")

    try:

        candidates = extract_skill_candidates(
            job["job_description"]
    )
    except Exception as e:
        print(f"Job {i} failed: {e}")
        continue


    for candidate in candidates:

        if candidate not in all_candidates:
            all_candidates.append(candidate)


print("\n==============================")
print("ALL UNIQUE CANDIDATES")
print("==============================\n")

for skill in sorted(all_candidates):
    print("-", skill)

normalized = normalize_candidates(all_candidates)

with open("candidate_output_full.txt", "w", encoding="utf-8") as file:
    for result in normalized:
        file.write(
            f"{result['candidate']} -> "
            f"{result['normalized']} "
            f"(known={result['known']})\n"
        )

print("\nSaved results to candidate_output_full.txt")        

print("\n==============================")
print("NORMALIZATION RESULTS")
print("==============================\n")



for result in normalized:
        print(
            f"{result['candidate']} -> "
            f"{result['normalized']} "
            f"(known={result['known']})"
        )    