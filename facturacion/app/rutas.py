# Rutas y lógica del microservicio de facturación
from flask import Blueprint, request, jsonify
from uuid import uuid4
import pika
import json
import requests
from app.modelos import db, Factura
from config import Config

bp = Blueprint('facturacion', __name__)

# CRUD Facturas
@bp.route('/facturas', methods=['POST'])
def crear_factura():
	data = request.get_json()
	factura = Factura(
		factura_id=str(uuid4()),
		cosecha_id=data['cosecha_id'],
		monto_total=data['monto_total'],
		pagado=data.get('pagado', False),
		metodo_pago=data.get('metodo_pago'),
		codigo_qr=data.get('codigo_qr')
	)
	db.session.add(factura)
	db.session.commit()
	return jsonify({'factura_id': factura.factura_id}), 201

@bp.route('/facturas', methods=['GET'])
def listar_facturas():
	facturas = Factura.query.all()
	return jsonify([
		{
			'factura_id': f.factura_id,
			'cosecha_id': f.cosecha_id,
			'monto_total': f.monto_total,
			'pagado': f.pagado,
			'fecha_emision': f.fecha_emision.isoformat() if f.fecha_emision else None,
			'metodo_pago': f.metodo_pago,
			'codigo_qr': f.codigo_qr
		} for f in facturas
	])

@bp.route('/facturas/<factura_id>', methods=['PUT'])
def actualizar_factura(factura_id):
	factura = Factura.query.get(factura_id)
	if not factura:
		return jsonify({'error': 'Factura no encontrada'}), 404
	data = request.get_json()
	factura.pagado = data.get('pagado', factura.pagado)
	factura.metodo_pago = data.get('metodo_pago', factura.metodo_pago)
	factura.codigo_qr = data.get('codigo_qr', factura.codigo_qr)
	db.session.commit()
	return jsonify({'mensaje': 'Factura actualizada'})

@bp.route('/facturas/<factura_id>', methods=['DELETE'])
def eliminar_factura(factura_id):
	factura = Factura.query.get(factura_id)
	if not factura:
		return jsonify({'error': 'Factura no encontrada'}), 404
	db.session.delete(factura)
	db.session.commit()
	return jsonify({'mensaje': 'Factura eliminada'})

# Worker/Consumidor de eventos de RabbitMQ para facturación automática
import threading
def consumir_facturacion():
	connection = pika.BlockingConnection(pika.URLParameters(Config.RABBITMQ_URL))
	channel = connection.channel()
	channel.queue_declare(queue='cola_facturacion')
	channel.queue_bind(exchange='cosechas', queue='cola_facturacion', routing_key='inventario_ok')

	PRECIOS = {
		'Arroz Oro': 120,
		'Café Premium': 300
	}

	def callback(ch, method, properties, body):
		mensaje = json.loads(body)
		cosecha_id = mensaje['cosecha_id']
		# Obtener detalles de la cosecha desde Central
		try:
			response = requests.get(f'{Config.CENTRAL_API}/cosechas/{cosecha_id}')
			if response.status_code != 200:
				ch.basic_ack(delivery_tag=method.delivery_tag)
				return
			cosecha = response.json()
			monto = cosecha['toneladas'] * PRECIOS.get(cosecha['producto'], 120)
			factura = Factura(
				factura_id=str(uuid4()),
				cosecha_id=cosecha_id,
				monto_total=monto,
				pagado=False
			)
			db.session.add(factura)
			db.session.commit()
			# Actualizar Central
			requests.put(f'{Config.CENTRAL_API}/cosechas/{cosecha_id}', json={
				'estado': 'FACTURADA',
				'factura_id': factura.factura_id
			})
		except Exception as e:
			print('Error en facturación automática:', e)
		ch.basic_ack(delivery_tag=method.delivery_tag)

	channel.basic_consume(queue='cola_facturacion', on_message_callback=callback)
	channel.start_consuming()

# Endpoint de salud
@bp.route('/health', methods=['GET'])
def health():
	return jsonify({'estado': 'saludable'}), 200
