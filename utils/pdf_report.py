import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(score, role, skills, missing, suggestions, roadmap):

    os.makedirs("reports", exist_ok=True)

    pdf_path = os.path.join("reports", "ATS_Report.pdf")

    pdf = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>CareerPilot AI Report</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>ATS Score:</b> {score}%", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Recommended Role:</b> {role}", styles["BodyText"]))

    elements.append(Paragraph("<br/>", styles["BodyText"]))

    elements.append(Paragraph("<b>Skills Found</b>", styles["Heading2"]))

    for skill in skills:
        elements.append(Paragraph(f"• {skill}", styles["BodyText"]))

    elements.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))

    for skill in missing:
        elements.append(Paragraph(f"• {skill}", styles["BodyText"]))

    elements.append(Paragraph("<b>AI Suggestions</b>", styles["Heading2"]))

    for item in suggestions:
        elements.append(Paragraph(f"• {item}", styles["BodyText"]))

    elements.append(Paragraph("<b>Career Roadmap</b>", styles["Heading2"]))

    for step in roadmap:
        elements.append(Paragraph(f"• {step}", styles["BodyText"]))

    pdf.build(elements)

    return pdf_path