from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import db, User

auth_bp = Blueprint("auth", __name__)


# ==========================
# Register
# ==========================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        college = request.form.get("college")
        course = request.form.get("course")
        graduation_year = request.form.get("graduation_year")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        # Validate
        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("auth.register"))

        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already exists!", "warning")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

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

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ==========================
# Login
# ==========================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["fullname"] = user.fullname

            flash(f"Welcome {user.fullname}!", "success")

            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid Email or Password", "danger")

        return redirect(url_for("auth.login"))

    return render_template("login.html")


# ==========================
# Logout
# ==========================

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "info")

    return redirect(url_for("auth.login"))