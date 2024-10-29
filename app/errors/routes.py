from flask import render_template
from app.errors import bp


@bp.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


@bp.errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), 403
