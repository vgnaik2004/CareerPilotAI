from flask import Blueprint, render_template, request, redirect, url_for, session
import os

from database import db, Resume

from utils.resume_parser import extract_text
from utils.skills import extract_skills
from utils.ats_score import calculate_ats
from utils.job_match import match_role
from utils.roadmap import get_roadmap
from utils.ai_suggestions import get_ai_suggestions

dashboard_bp = Blueprint("dashboard", __name__)


# =====================================
# Dashboard Home
# =====================================

@dashboard_bp.route("/")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("index.html")


# =====================================
# Resume Upload
# =====================================

@dashboard_bp.route("/upload", methods=["POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if "resume" not in request.files:
        return "No Resume Uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please Select Resume"

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, file.filename)

    file.save(filepath)

    # -------------------------
    # Resume Analysis
    # -------------------------

    resume_text = extract_text(filepath)

    skills = extract_skills(resume_text)

    score, suggestions = calculate_ats(resume_text)

    role = request.form.get(
        "role",
        "Python Developer"
    )

    job_match, found, missing = match_role(
        role,
        skills
    )

    roadmap = get_roadmap(role)

    ai_suggestions = get_ai_suggestions(
        score,
        missing
    )

    # -------------------------
    # Save History
    # -------------------------

    history = Resume(

        filename=file.filename,

        ats_score=score,

        job_role=role,

        user_id=session["user_id"]

    )

    db.session.add(history)

    db.session.commit()

    # -------------------------
    # Dashboard
    # -------------------------

    return render_template(

        "dashboard.html",

        score=score,

        role=role,

        job_match=job_match,

        skills=found,

        missing=missing,

        roadmap=roadmap,

        suggestions=ai_suggestions,

        resume_text=resume_text

    )