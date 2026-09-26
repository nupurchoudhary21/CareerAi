import json
import requests
from .skill_normalizer import normalize_candidates


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def extract_skill_candidates(job_description):

    prompt = f"""
You are extracting skills from a job description.

Read ONLY the text between <JOB_DESCRIPTION> and </JOB_DESCRIPTION>.

Return ONLY a JSON object with exactly one key: "skills".

The value of "skills" must be a JSON array of skill names.

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
- Do NOT return generic words such as "certified", "certification",
  "experience", "knowledge", "candidate", "professional", or "years".
- Do NOT return category names as skills.
- Do NOT return skill-to-value mappings.
- Do NOT create additional JSON keys.

Example:

If the job description says:
"Experience with Python, Django, PostgreSQL and Docker."

Return exactly:

{{
  "skills": ["Python", "Django", "PostgreSQL", "Docker"]
}}

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
        },
        timeout=120
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
            skills = candidates.get("skills",[])

            if isinstance(skills, list):
                return skills

            return []

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

    normalized = normalize_candidates(candidates)

    print("\nNORMALIZED RESULTS:\n")

    for result in normalized:

        print(
            f"{result['candidate']} "
            f"-> {result['normalized']} "
            f"(known={result['known']})"
        )    