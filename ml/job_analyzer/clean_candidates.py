from pathlib import Path

INPUT_FILE = Path("candidate_output.txt")
OUTPUT_FILE = Path("cleaned_candidates.txt")

candidates = set()

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for line in file:
        if "->" not in line:
            continue

        candidate = line.split("->", 1)[0].strip()

        if candidate:
            candidates.add(candidate)

IGNORE_PHRASES = {
    "frameworks",
    "testing frameworks",
    "communication skills",
    "organizational skills",
    "agile experience",
    "strong understanding of design principles and design patterns",    
}  

cleaned_candidates = sorted(
    candidate
    for candidate in candidates 
    if candidate.lower() not in IGNORE_PHRASES 
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    for candidate in cleaned_candidates:
        file.write(candidate + "\n")


print(f"Orginial unique candidates: {len(candidates)}")
print(f"Cleaned candidates: {len(cleaned_candidates)}")
print(f"Removed: {len(candidates) - len(cleaned_candidates)}")
print(f"Saved to: {OUTPUT_FILE}")


