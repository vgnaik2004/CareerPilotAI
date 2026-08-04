from flask import Blueprint, render_template, session, redirect, url_for
from database import User

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    return render_template(
        "profile.html",
        user=user
    )