import re

def clean_text(raw_text: str) -> str:
    # cleaned = re.sub(r'\n+', '\n', raw_text)  # collapse multiple newlines
    # cleaned = "\n".join(line.strip() for line in cleaned.splitlines())  # trim each line
    # cleaned = re.sub(r' {2,}', ' ', cleaned)  # remove extra spaces
    # #cleaned = re.sub(r'^\d+$', '', cleaned, flags=re.MULTILINE)  # remove standalone numbers
    # #cleaned = re.sub(r'^\d{2,}$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'\n+', '\n', raw_text)

    # Trim whitespaces from start and end of each line
    cleaned = "\n".join(line.strip() for line in cleaned.splitlines())

    # Collapse multiple spaces inside text (not at line boundaries)
    cleaned = re.sub(r' {2,}', ' ', cleaned)

    # Do NOT remove digit-only lines or short lines — they can be valid answers
    return cleaned