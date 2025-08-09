# Modelos de datos para el microservicio central
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Agricultor(db.Model):
	__tablename__ = 'agricultores'
	agricultor_id = db.Column(db.String(36), primary_key=True)
	nombre = db.Column(db.String(100), nullable=False)
	finca = db.Column(db.String(100), nullable=False)
	ubicacion = db.Column(db.String(100), nullable=False)
	correo = db.Column(db.String(150), unique=True, nullable=False)
	fecha_registro = db.Column(db.DateTime, server_default=db.func.now())

class Cosecha(db.Model):
	__tablename__ = 'cosechas'
	cosecha_id = db.Column(db.String(36), primary_key=True)
	agricultor_id = db.Column(db.String(36), db.ForeignKey('agricultores.agricultor_id'), nullable=False)
	producto = db.Column(db.String(50), nullable=False)
	toneladas = db.Column(db.Float, nullable=False)
	estado = db.Column(db.String(20), default='REGISTRADA')
	creado_en = db.Column(db.DateTime, server_default=db.func.now())
	factura_id = db.Column(db.String(36), nullable=True)
	__table_args__ = (
		db.CheckConstraint('toneladas >= 0', name='check_toneladas_nonnegative'),
	)
