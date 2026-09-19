import csv

def load_jobs(file_path):

    jobs = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            jobs.append({
                "job_title": row["Job Title"],
                "job_description": row["Job Description"]
            })

    return jobs        