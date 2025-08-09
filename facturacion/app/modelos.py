# Modelos de datos para el microservicio de facturación
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Factura(db.Model):
	__tablename__ = 'facturas'
	factura_id = db.Column(db.String(36), primary_key=True)
	cosecha_id = db.Column(db.String(36), nullable=False)
	monto_total = db.Column(db.Float, nullable=False)
	pagado = db.Column(db.Boolean, default=False)
	fecha_emision = db.Column(db.DateTime, server_default=db.func.now())
	metodo_pago = db.Column(db.String(30), nullable=True)
	codigo_qr = db.Column(db.Text, nullable=True)
