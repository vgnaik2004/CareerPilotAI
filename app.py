from flask import Flask, render_template, request
import os

from resume_parser import extract_text
from skills import extract_skills
from ats_score import calculate_ats
from job_match import match_role

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No Resume Uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please Select Resume"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    # ----------------------------------
    # Extract Resume Text
    # ----------------------------------

    resume_text = extract_text(filepath)

    # ----------------------------------
    # Extract Skills
    # ----------------------------------

    skills = extract_skills(resume_text)

    # ----------------------------------
    # ATS Score
    # ----------------------------------

    score, suggestions = calculate_ats(resume_text)

    # ----------------------------------
    # Selected Job Role
    # ----------------------------------

    role = request.form.get("role", "Frontend Developer")

    # ----------------------------------
    # Job Match
    # ----------------------------------

    match_percentage, found, missing = match_role(role, skills)

    # ----------------------------------
    # Send Data to Dashboard
    # ----------------------------------

    return render_template(

        "dashboard.html",

        score=score,

        role=role,

        job_match=match_percentage,

        skills=found,

        missing=missing,

        suggestions=suggestions,

        resume_text=resume_text

    )


if __name__ == "__main__":
    app.run(debug=True)