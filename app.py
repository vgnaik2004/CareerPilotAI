from flask import send_file
from utils.pdf_report import generate_pdf
from utils.interview_questions import get_interview_questions
from utils.ai_suggestions import get_ai_suggestions
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from database import db, User, Resume
from sqlalchemy import func

from utils.resume_parser import extract_text
from utils.skills import extract_skills
from utils.ats_score import calculate_ats
from utils.job_match import match_role
from utils.roadmap import get_roadmap

app = Flask(__name__)

# -------------------------------
# Configuration
# -------------------------------
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Secret Key
app.secret_key = Config.SECRET_KEY

# Upload Folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create Database
with app.app_context():
    db.create_all()

# -----------------------------------
# Home Page
# -----------------------------------

@app.route("/")
def home():

    if "user_id" in session:
        return render_template("index.html")

    return redirect(url_for("login"))


# -----------------------------------
# Register Page
# -----------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # Check password match
        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # Check existing user
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!", "warning")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(
            fullname=fullname,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! Please Login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")

# -----------------------------------
# Login Page
# -----------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["fullname"] = user.fullname

            return redirect(url_for("home"))

        flash("Invalid Email or Password", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

# -----------------------------------
# Upload Resume
# -----------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "resume" not in request.files:
        return "No Resume Uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please Select Resume"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    # Extract Resume Text
    resume_text = extract_text(filepath)

    # Extract Skills
    skills = extract_skills(resume_text)

    # ATS Score
    score, suggestions = calculate_ats(resume_text)

    # Selected Job Role
    role = request.form.get("role", "Frontend Developer")
    # Job Match
    job_match, found, missing = match_role(role, skills)
    roadmap = get_roadmap(role)
    ai_suggestions = get_ai_suggestions(score, missing)
    

    # -----------------------------
    # Save Resume History
    # -----------------------------
    new_resume = Resume(
        filename=file.filename,
        ats_score=score,
        job_role=role,
        user_id=session["user_id"]
    )

    db.session.add(new_resume)
    db.session.commit()

    return render_template(
    "dashboard.html",
    score=score,
    role=role,
    job_match=job_match,
    skills=found,
    missing=missing,
    suggestions=ai_suggestions,
    resume_text=resume_text,
    roadmap=roadmap,
)

# ===================================
# Resume History
# ===================================

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    resumes = Resume.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Resume.upload_date.desc()
    ).all()

    return render_template(
        "history.html",
        resumes=resumes
    )

# ===================================
# Profile Page
# ===================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    return render_template(
        "profile.html",
        user=user
    )


# ===================================
# Admin Dashboard
# ===================================

@app.route("/admin")
def admin():

    total_users = User.query.count()

    total_resumes = Resume.query.count()

    average_score = db.session.query(
        func.avg(Resume.ats_score)
    ).scalar()

    return render_template(
        "admin.html",
        total_users=total_users,
        total_resumes=total_resumes,
        average_score=round(average_score or 0, 2)
    )

# ===================================
# Download PDF Report
# ===================================

@app.route("/download-report")
def download_report():

    roadmap = [
        "Improve Missing Skills",
        "Build More Projects",
        "Practice Interview Questions",
        "Apply for Jobs"
    ]

    generate_pdf(
        "reports/ATS_Report.pdf",
        score=85,
        role="Python Developer",
        skills=["Python", "Flask", "SQL"],
        missing=["Docker", "AWS"],
        suggestions=[
            "Add more projects",
            "Improve ATS keywords"
        ],
        roadmap=roadmap
    )

    return send_file(
        "reports/ATS_Report.pdf",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)