from flask import render_template, request, current_app
from tweepy.models import ResultSet
from tweetsourcing.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.error(f'404 Error to {request.url} with {request.method}')
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f'500 Error to {request.url} with {request.method}')
    return render_template('errors/500.html'), 500

@bp.route("no-results")
def no_results():
    return render_template('errors/no-results.html')