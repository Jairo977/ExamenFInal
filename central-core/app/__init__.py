from flask import Flask
from app.modelos import db
from app.rutas import bp
from config import Config

def create_app():
    import time
    import sqlalchemy
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(bp)
    # Retry DB connection
    max_retries = 10
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            break
        except sqlalchemy.exc.OperationalError as e:
            print(f"[Central-Core] DB connection failed (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(3)
    else:
        raise Exception("[Central-Core] Could not connect to PostgreSQL after several attempts.")
    return app
