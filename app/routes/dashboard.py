from flask import Blueprint


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    return """
    <h1>Academic Workload Balancer</h1>
    <p>Flask application is running successfully!</p>
    """