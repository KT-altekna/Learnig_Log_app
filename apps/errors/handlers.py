from flask import render_template, current_app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        current_app.logger.exception("404 Not Found")
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        current_app.logger.exception("500 Internal Server Error")
        return render_template("errors/500.html"), 500
