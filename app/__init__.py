from flask import Flask
from app.routes.review_routes import review_bp


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(review_bp)

    return app
