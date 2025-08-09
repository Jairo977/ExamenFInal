from flask import Flask
from app.modelos import db
from app.rutas import bp
from config import Config
import threading

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    # Aquí puedes iniciar el consumidor de RabbitMQ en un hilo separado si lo necesitas
    # threading.Thread(target=consumir_inventario, daemon=True).start()
    return app
