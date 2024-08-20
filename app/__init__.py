from flask import Flask
from app.routes.review_routes import review_bp
from app.routes.user_generated_content_routes import ugc_bp


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(review_bp)
    app.register_blueprint(ugc_bp)

    return app
