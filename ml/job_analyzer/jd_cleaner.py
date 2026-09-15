import re

def clean_job_description(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    text = "\n".join(
       line.strip()
       for line in text.splitlines() 
    )

    return text.strip()