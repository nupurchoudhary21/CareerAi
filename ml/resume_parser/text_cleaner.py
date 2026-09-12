import re

def clean_text(text):
    
    # Replace multiple spaces with a single space 
    text = re.sub(r"[ \t]+", " ", text)

    # Replace excessive blank lines 
    text = re.sub(r"\n\s*\n+", "\n", text)

    #replace spaces at the beginning/end of the lines 
    text = "\n".join(line.strip() for line in text.splitlines())

    return text.strip()

