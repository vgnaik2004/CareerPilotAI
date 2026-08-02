from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# =====================================
# User Table
# =====================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship with Resume table
    resumes = db.relationship(
        "Resume",
        backref="user",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.email}>"


# =====================================
# Resume Table
# =====================================

class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(
        db.String(200),
        nullable=False
    )

    ats_score = db.Column(
        db.Integer,
        nullable=False
    )

    job_role = db.Column(
        db.String(100),
        nullable=False
    )

    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Resume {self.filename}>"