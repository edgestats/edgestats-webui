from flask import Blueprint, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFError

bp_error = Blueprint("error", __name__, url_prefix="/error/")


@bp_error.app_errorhandler(CSRFError)
def error_csrf(error):
    """Custom 400 Error Page"""
    return render_template("error.html", error=error), 400


@bp_error.app_errorhandler(404)
def error_404(error):
    """Custom 404 Error Page"""
    return render_template("error.html", error=error), 404


@bp_error.app_errorhandler(500)
def error_500(error):
    """Custom 500 Error Page"""
    return render_template("error.html", error=error), 500
