"""Entry point duy nhất: python run.py"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Disable use_reloader to prevent Windows process/tab spawning loops
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)