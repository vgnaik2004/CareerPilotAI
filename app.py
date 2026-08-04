from flask import send_file
from sqlalchemy import func
from flask import Flask
from config import Config
from database import db

# ===============================
# Import Blueprints
# ===============================

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.profile import profile_bp
from routes.history import history_bp
from routes.admin import admin_bp
from routes.report import report_bp

# ===============================
# Create Flask App
# ===============================

app = Flask(__name__)

# ===============================
# Load Configuration
# ===============================

app.config.from_object(Config)

# ===============================
# Initialize Database
# ===============================

db.init_app(app)

# ===============================
# Create Database Tables
# ===============================

with app.app_context():
    db.create_all()

# ===============================
# Register Blueprints
# ===============================

app.register_blueprint(auth_bp)

app.register_blueprint(dashboard_bp)

app.register_blueprint(profile_bp)

app.register_blueprint(history_bp)

app.register_blueprint(admin_bp)

app.register_blueprint(report_bp)

# ===============================
# Home Route
# ===============================

@app.route("/")
def home():
    """
    Redirect to Dashboard.
    Dashboard blueprint handles
    login checking.
    """

    from flask import redirect, url_for

    return redirect(url_for("dashboard.dashboard"))


# ===============================
# Health Check
# ===============================


# ===============================
# 404 Error
# ===============================

@app.errorhandler(404)
def page_not_found(error):

    return (
        "404 - Page Not Found",
        404
    )


# ===============================
# 500 Error
# ===============================

@app.errorhandler(500)
def internal_server(error):

    return (
        "500 - Internal Server Error",
        500
    )

# ==========================================
# Authentication
# ==========================================

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ------------------------------------------
# Register
# ------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        college = request.form.get("college")
        course = request.form.get("course")
        graduation_year = request.form.get("graduation_year")

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validate Password
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # Check Existing User
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!", "warning")
            return redirect(url_for("register"))

        # Encrypt Password
        hashed_password = generate_password_hash(password)

        # Create User
        new_user = User(
            fullname=fullname,
            email=email,
            mobile=mobile,
            college=college,
            course=course,
            graduation_year=graduation_year,
            bio="",
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! Please Login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


# ------------------------------------------
# Login
# ------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:

            if check_password_hash(user.password, password):

                session["user_id"] = user.id
                session["fullname"] = user.fullname

                flash(
                    f"Welcome {user.fullname}!",
                    "success"
                )

                return redirect(url_for("dashboard"))

        flash(
            "Invalid Email or Password",
            "danger"
        )

        return redirect(url_for("login"))

    return render_template("login.html")


# ------------------------------------------
# Logout
# ------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged Out Successfully",
        "info"
    )

    return redirect(url_for("login"))


# ==========================================
# Dashboard
# ==========================================

import os

from utils.resume_parser import extract_text
from utils.skills import extract_skills
from utils.ats_score import calculate_ats
from utils.job_match import match_role
from utils.roadmap import get_roadmap
from utils.ai_suggestions import get_ai_suggestions


@app.route("/")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    resumes = Resume.query.filter_by(
        user_id=user.id
    ).order_by(
        Resume.upload_date.desc()
    ).all()

    return render_template(
        "dashboard.html",
        user=user,
        resumes=resumes
    )


# ==========================================
# Resume Upload
# ==========================================

@app.route("/upload", methods=["POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "resume" not in request.files:

        flash("Please upload a resume.", "warning")

        return redirect(url_for("dashboard"))

    file = request.files["resume"]

    if file.filename == "":

        flash("No file selected.", "warning")

        return redirect(url_for("dashboard"))

    upload_folder = app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(
        upload_folder,
        file.filename
    )

    file.save(filepath)

    # -----------------------------------
    # Resume Analysis
    # -----------------------------------

    resume_text = extract_text(filepath)

    skills = extract_skills(resume_text)

    score, ats_suggestions = calculate_ats(
        resume_text
    )

    role = request.form.get(
        "role",
        "Python Developer"
    )

    job_match, found_skills, missing_skills = match_role(
        role,
        skills
    )

    roadmap = get_roadmap(role)

    ai_suggestions = get_ai_suggestions(
        score,
        missing_skills
    )

    # -----------------------------------
    # Generate PDF Report
    # -----------------------------------

    generate_pdf(
        score,
        role,
        found_skills,
        missing_skills,
        ai_suggestions,
        roadmap
    )

    # -----------------------------------
    # Save Resume
    # -----------------------------------

    history = Resume(
        filename=file.filename,
        ats_score=score,
        job_role=role,
        user_id=session["user_id"]
    )

    db.session.add(history)
    db.session.commit()

    return render_template(
        "dashboard.html",
        score=score,
        role=role,
        resume_text=resume_text,
        skills=found_skills,
        missing=missing_skills,
        roadmap=roadmap,
        suggestions=ai_suggestions,
        ats_suggestions=ats_suggestions,
        resumes=Resume.query.filter_by(
            user_id=session["user_id"]
        ).all()
    )
# ==========================================
# Delete Resume
# ==========================================

@app.route("/delete_resume/<int:resume_id>")
def delete_resume(resume_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=session["user_id"]
    ).first()

    if resume:

        db.session.delete(resume)

        db.session.commit()

        flash(
            "Resume deleted successfully.",
            "success"
        )

    return redirect(url_for("dashboard"))


# ==========================================================
# Profile
# ==========================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    total_resumes = Resume.query.filter_by(
        user_id=user.id
    ).count()

    latest_resume = Resume.query.filter_by(
        user_id=user.id
    ).order_by(
        Resume.upload_date.desc()
    ).first()

    avg_score = 0

    resumes = Resume.query.filter_by(
        user_id=user.id
    ).all()

    if resumes:

        total = sum(r.ats_score for r in resumes)

        avg_score = round(total / len(resumes))

    return render_template(

        "profile.html",

        user=user,

        total_resumes=total_resumes,

        latest_resume=latest_resume,

        avg_score=avg_score

    )


# ==========================================================
# Update Profile
# ==========================================================

@app.route("/update_profile", methods=["POST"])
def update_profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    user.fullname = request.form.get("fullname")

    user.mobile = request.form.get("mobile")

    user.college = request.form.get("college")

    user.course = request.form.get("course")

    user.graduation_year = request.form.get(
        "graduation_year"
    )

    user.bio = request.form.get("bio")

    db.session.commit()

    flash(
        "Profile Updated Successfully!",
        "success"
    )

    return redirect(url_for("profile"))


# ==========================================================
# Change Password
# ==========================================================

@app.route("/change_password", methods=["POST"])
def change_password():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    current = request.form.get("current_password")

    new = request.form.get("new_password")

    confirm = request.form.get("confirm_password")

    if not check_password_hash(
        user.password,
        current
    ):

        flash(
            "Current Password is Incorrect",
            "danger"
        )

        return redirect(url_for("profile"))

    if new != confirm:

        flash(
            "Passwords do not match",
            "danger"
        )

        return redirect(url_for("profile"))

    user.password = generate_password_hash(new)

    db.session.commit()

    flash(
        "Password Changed Successfully!",
        "success"
    )

    return redirect(url_for("profile"))


# ==========================================================
# Resume History
# ==========================================================

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


# ==========================================================
# View Resume Details
# ==========================================================

@app.route("/history/<int:resume_id>")
def history_details(resume_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    resume = Resume.query.filter_by(

        id=resume_id,

        user_id=session["user_id"]

    ).first_or_404()

    return render_template(

        "history_details.html",

        resume=resume

    )

# ==========================================================
# Admin Dashboard
# ==========================================================

from sqlalchemy import func
from utils.pdf_report import generate_pdf


@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Optional: Replace this with a proper admin-role check
    if session.get("user_id") != 1:
        flash("Access Denied!", "danger")
        return redirect(url_for("dashboard"))

    total_users = User.query.count()

    total_resumes = Resume.query.count()

    average_score = db.session.query(
        func.avg(Resume.ats_score)
    ).scalar()

    average_score = round(average_score or 0)

    highest_resume = Resume.query.order_by(
        Resume.ats_score.desc()
    ).first()

    recent_users = User.query.order_by(
        User.created_at.desc()
    ).limit(5).all()

    recent_resumes = Resume.query.order_by(
        Resume.upload_date.desc()
    ).limit(10).all()

    chart_labels = []
    chart_scores = []

    top_resumes = Resume.query.order_by(
        Resume.upload_date.asc()
    ).limit(10).all()

    for item in top_resumes:
        chart_labels.append(item.filename)
        chart_scores.append(item.ats_score)

    return render_template(

        "admin.html",

        total_users=total_users,

        total_resumes=total_resumes,

        average_score=average_score,

        highest_resume=highest_resume,

        recent_users=recent_users,

        recent_resumes=recent_resumes,

        chart_labels=chart_labels,

        chart_scores=chart_scores

    )


# ==========================================================
# Download PDF Report
# ==========================================================

from flask import send_file
import os

@app.route("/download-report")
def download_report():

    if "user_id" not in session:
        return redirect(url_for("login"))

    pdf_path = os.path.join("reports", "ATS_Report.pdf")

    if not os.path.exists(pdf_path):
        flash("PDF report not found!", "danger")
        return redirect(url_for("dashboard"))

    return send_file(
        pdf_path,
        as_attachment=True
    )




# ==========================================================
# Delete User (Admin)
# ==========================================================

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("user_id") != 1:
        flash("Access Denied!", "danger")
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(user_id)

    Resume.query.filter_by(
        user_id=user.id
    ).delete()

    db.session.delete(user)

    db.session.commit()

    flash(
        "User Deleted Successfully!",
        "success"
    )

    return redirect(url_for("admin"))


# ==========================================================
# Dashboard Analytics API
# ==========================================================

@app.route("/analytics")
def analytics():

    if "user_id" not in session:
        return redirect(url_for("login"))

    resumes = Resume.query.filter_by(
        user_id=session["user_id"]
    ).all()

    scores = [r.ats_score for r in resumes]

    labels = [r.filename for r in resumes]

    return {

        "labels": labels,

        "scores": scores

    }


# ==========================================================
# About Page
# ==========================================================

@app.route("/about")
def about():

    return render_template("about.html")


# ==========================================================
# Contact Page
# ==========================================================

@app.route("/contact")
def contact():

    return render_template("contact.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )


