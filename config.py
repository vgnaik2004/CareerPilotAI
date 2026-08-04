import os

class Config:

    SECRET_KEY = "careerpilot_ai_secret_key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///careerpilot.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"

    REPORT_FOLDER = "reports"