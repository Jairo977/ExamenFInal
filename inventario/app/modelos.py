# Modelos de datos para el microservicio inventario
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Insumo(db.Model):
	__tablename__ = 'insumos'
	insumo_id = db.Column(db.String(36), primary_key=True)
	nombre_insumo = db.Column(db.String(100), unique=True, nullable=False)
	stock = db.Column(db.Integer, default=0)
	unidad_medida = db.Column(db.String(10), default='kg')
	categoria = db.Column(db.String(30), nullable=False)
	ultima_actualizacion = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
