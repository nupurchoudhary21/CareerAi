import csv
from pathlib import Path

from ml.job_analyzer.candidate_classifier import classify_candidate


INPUT_FILE = Path("cleaned_candidates.txt")
OUTPUT_FILE = Path("classified_candidates.csv")


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    candidates = [line.strip() for line in file if line.strip()]


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Candidate", "Classification"])

    for candidate in candidates:
        classification = classify_candidate(candidate)
        writer.writerow([candidate, classification])


print(f"Total candidates: {len(candidates)}")
print(f"Classification saved to: {OUTPUT_FILE}")