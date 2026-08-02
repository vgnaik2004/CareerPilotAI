from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(filename, score, role, skills, missing, suggestions, roadmap):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>CareerPilot AI Report</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>ATS Score:</b> {score}%", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Job Role:</b> {role}", styles["BodyText"]))

    # Skills Found
    elements.append(Paragraph("<b>Skills Found</b>", styles["Heading2"]))

    for skill in skills:
        elements.append(Paragraph(f"• {skill}", styles["BodyText"]))

    # Missing Skills
    elements.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))

    for skill in missing:
        elements.append(Paragraph(f"• {skill}", styles["BodyText"]))

    # AI Suggestions
    elements.append(Paragraph("<b>AI Suggestions</b>", styles["Heading2"]))

    for item in suggestions:
        elements.append(Paragraph(f"• {item}", styles["BodyText"]))

    # Career Roadmap
    elements.append(Paragraph("<b>Career Roadmap</b>", styles["Heading2"]))

    for step in roadmap:
        elements.append(Paragraph(f"• {step}", styles["BodyText"]))

    pdf.build(elements)