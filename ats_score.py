import re

def calculate_ats(text):

    score = 0
    suggestions = []

    # -----------------------
    # Email
    # -----------------------
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    if re.search(email_pattern, text):
        score += 10
    else:
        suggestions.append("Add Email Address")

    # -----------------------
    # Phone Number
    # -----------------------
    # Remove everything except digits
    clean_number = re.sub(r"\D", "", text)

    # Check if there are at least 10 consecutive digits
    if len(clean_number) >= 10:
        score += 10
    else:
        suggestions.append("Add Phone Number")

    # -----------------------
    # Education
    # -----------------------
    if "education" in text.lower():
        score += 15
    else:
        suggestions.append("Add Education Section")

    # -----------------------
    # Skills
    # -----------------------
    if "skills" in text.lower():
        score += 20
    else:
        suggestions.append("Add Skills Section")

    # -----------------------
    # Projects
    # -----------------------
    if "project" in text.lower():
        score += 20
    else:
        suggestions.append("Add Projects")

    # -----------------------
    # Certifications
    # -----------------------
    if "certification" in text.lower():
        score += 10
    else:
        suggestions.append("Add Certification Section")

    # -----------------------
    # GitHub
    # -----------------------
    if "github" in text.lower():
        score += 10
    else:
        suggestions.append("Add GitHub Profile")

    # -----------------------
    # LinkedIn
    # -----------------------
    if "linkedin" in text.lower():
        score += 5
    else:
        suggestions.append("Add LinkedIn Profile")

    return score, suggestions