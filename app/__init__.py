import json
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app() -> Flask:
    load_dotenv(BASE_DIR / ".env")

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    with open(BASE_DIR / "config" / "rules.json", encoding="utf-8") as f:
        app.config["RULES"] = json.load(f)
    app.config["EXPORT_DIR"] = BASE_DIR / "exports"

    from app.api.routes_home import bp as home_bp
    from app.api.routes_scan import bp as scan_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(scan_bp)
    return app
