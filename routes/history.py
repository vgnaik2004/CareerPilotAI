from flask import Blueprint, render_template, session, redirect, url_for
from database import Resume

history_bp = Blueprint("history", __name__)

@history_bp.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    resumes = Resume.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Resume.upload_date.desc()
    ).all()

    return render_template(
        "history.html",
        resumes=resumes
    )