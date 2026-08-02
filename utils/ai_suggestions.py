def get_ai_suggestions(score, missing_skills):

    suggestions = []

    if score < 60:
        suggestions.append("Improve your resume formatting.")
        suggestions.append("Add more technical skills.")
        suggestions.append("Include projects and internships.")

    elif score < 80:
        suggestions.append("Add certifications.")
        suggestions.append("Improve project descriptions.")
        suggestions.append("Use ATS-friendly keywords.")

    else:
        suggestions.append("Excellent ATS score.")
        suggestions.append("Keep your resume updated.")
        suggestions.append("Tailor your resume for each job.")

    if missing_skills:
        suggestions.append("Learn these missing skills:")

        for skill in missing_skills:
            suggestions.append(skill)

    return suggestions