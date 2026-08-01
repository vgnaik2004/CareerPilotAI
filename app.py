from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from database import db, User

from utils.resume_parser import extract_text
from utils.skills import extract_skills
from utils.ats_score import calculate_ats
from utils.job_match import match_role

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

if __name__ == "__main__":
    app.run(debug=True)