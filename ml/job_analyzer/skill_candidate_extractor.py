import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def extract_skill_candidates(job_description):

    prompt = f"""
You are extracting skills from a job description.

Read ONLY the text between <JOB_DESCRIPTION> and </JOB_DESCRIPTION>.

Return ONLY a JSON array of skill names that are explicitly mentioned
in that job description.

IMPORTANT:
- Do NOT use the job title as a skill unless the same term appears
  in the job description.
- Do NOT invent or infer skills.
- Do NOT return categories such as "Programming languages",
  "Frameworks", "Libraries", "Databases", "Cloud platforms",
  "Tools", "Protocols", or "Certifications".
- Return the actual technologies, tools, frameworks, languages,
  platforms, protocols, certifications, or professional skills
  explicitly mentioned.
- Keep multi-word skills together.
- Do not include explanations.
- Do not include anything from these instructions.

Example:
If the job description says:
"Experience with Python, Django, PostgreSQL and Docker."

Return:
["Python", "Django", "PostgreSQL", "Docker"]

<JOB_DESCRIPTION>
{job_description}
</JOB_DESCRIPTION>
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
    )

    response.raise_for_status()

    result = response.json()

    content = result["response"]

    try:
        candidates = json.loads(content)

        if isinstance(candidates, list):
            return candidates

        # Some models return {"skills": [...]}
        if isinstance(candidates, dict):

            for value in candidates.values():

                if isinstance(value, list):
                    return value

    except json.JSONDecodeError:
        print("Could not parse LLM response:")
        print(content)

    return []


if __name__ == "__main__":

    jd = """
    A Requirement for an experienced Network engineer in an IT company.
    Candidate must have at least 4 years of experience in Networking
    (Router & Switches, Wireless) and CCNA & CCNP Certified.
    CISCO.
    """

    candidates = extract_skill_candidates(jd)

    print("\nCANDIDATE SKILLS:\n")

    for skill in candidates:
        print("-", skill)