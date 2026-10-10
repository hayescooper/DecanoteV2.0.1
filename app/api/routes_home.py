from flask import Blueprint, current_app, render_template

bp = Blueprint("home", __name__)


@bp.get("/")
def home():
    chunk_size = current_app.config["RULES"]["chunk_size"]
    return render_template("home.html", chunk_size=chunk_size)
