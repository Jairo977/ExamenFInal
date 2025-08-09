from flask import Flask
from app.modelos import db
from app.rutas import bp
from config import Config
import threading

def create_app():
    import time
    import sqlalchemy
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
            print(f"[Facturacion] DB connection failed (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(3)
    else:
        raise Exception("[Facturacion] Could not connect to MariaDB after several attempts.")
    # Iniciar el consumidor de RabbitMQ en un hilo separado
    from app.rutas import consumir_facturacion
    threading.Thread(target=consumir_facturacion, daemon=True).start()
    return app
