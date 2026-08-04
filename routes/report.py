from flask import Blueprint

report_bp = Blueprint("report", __name__)

@report_bp.route("/report")
def report():
    return "Report Module"