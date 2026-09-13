import re

# email
def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None

# phone

def extract_phone(text):
    pattern = r"(?:\+91[-\s]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


def extract_linkedin(text):

    pattern = r"(?:https?://)?(?:www\.)?linkedin\.com/in.[A-Za-z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()

    return None


def extract_github(text):

    pattern = r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()

    return None



def extract_portfolio(text):

    urls = re.findall(
        r"https?://[^\s]+",
        text
    )

    for url in urls:
        url = url.rstrip(".,)")

        if "linkedin.com" not in url.lower() \
            and "github.com" not in url.lower():

            return url

    return None 



def extract_contact_info(text):

    contact = {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "portfolio": extract_portfolio(text)
    }

    return contact