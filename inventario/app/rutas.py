# Rutas y lógica del microservicio inventario
from flask import Blueprint, request, jsonify
from uuid import uuid4
import pika
import json
from app.modelos import db, Insumo
from config import Config

bp = Blueprint('inventario', __name__)

# CRUD de Insumos
@bp.route('/insumos', methods=['POST'])
def crear_insumo():
	data = request.get_json()
	insumo = Insumo(
		insumo_id=str(uuid4()),
		nombre_insumo=data['nombre_insumo'],
		stock=data.get('stock', 0),
		unidad_medida=data.get('unidad_medida', 'kg'),
		categoria=data.get('categoria', 'General')
	)
	db.session.add(insumo)
	db.session.commit()
	return jsonify({'insumo_id': insumo.insumo_id}), 201

@bp.route('/insumos', methods=['GET'])
def listar_insumos():
	insumos = Insumo.query.all()
	return jsonify([
		{
			'insumo_id': i.insumo_id,
			'nombre_insumo': i.nombre_insumo,
			'stock': i.stock,
			'unidad_medida': i.unidad_medida,
			'categoria': i.categoria
		} for i in insumos
	])

@bp.route('/insumos/<insumo_id>', methods=['PUT'])
def actualizar_insumo(insumo_id):
	insumo = Insumo.query.get(insumo_id)
	if not insumo:
		return jsonify({'error': 'Insumo no encontrado'}), 404
	data = request.get_json()
	insumo.nombre_insumo = data.get('nombre_insumo', insumo.nombre_insumo)
	insumo.stock = data.get('stock', insumo.stock)
	insumo.unidad_medida = data.get('unidad_medida', insumo.unidad_medida)
	insumo.categoria = data.get('categoria', insumo.categoria)
	db.session.commit()
	return jsonify({'mensaje': 'Insumo actualizado'})

@bp.route('/insumos/<insumo_id>', methods=['DELETE'])
def eliminar_insumo(insumo_id):
	insumo = Insumo.query.get(insumo_id)
	if not insumo:
		return jsonify({'error': 'Insumo no encontrado'}), 404
	db.session.delete(insumo)
	db.session.commit()
	return jsonify({'mensaje': 'Insumo eliminado'})

# Worker/Consumidor de eventos de RabbitMQ
import threading
def consumir_inventario():
	connection = pika.BlockingConnection(pika.URLParameters(Config.RABBITMQ_URL))
	channel = connection.channel()
	channel.queue_declare(queue='cola_inventario')
	channel.queue_bind(exchange='cosechas', queue='cola_inventario', routing_key='nueva')

	def callback(ch, method, properties, body):
		mensaje = json.loads(body)
		payload = mensaje['payload']
		toneladas = payload['toneladas']
		producto = payload['producto']
		# Actualizar inventario
		semilla = Insumo.query.filter_by(nombre_insumo=f'Semilla {producto}').first()
		fertilizante = Insumo.query.filter_by(nombre_insumo='Fertilizante N-PK').first()
		if semilla:
			semilla.stock -= int(toneladas * 5)
		if fertilizante:
			fertilizante.stock -= int(toneladas * 2)
		db.session.commit()
		# Publicar confirmación
		ch.basic_publish(
			exchange='cosechas',
			routing_key='inventario_ok',
			body=json.dumps({
				'event_id': str(uuid4()),
				'event_type': 'inventario_ajustado',
				'cosecha_id': payload['cosecha_id'],
				'status': 'OK'
			})
		)
		ch.basic_ack(delivery_tag=method.delivery_tag)

	channel.basic_consume(queue='cola_inventario', on_message_callback=callback)
	channel.start_consuming()

# Endpoint de salud
@bp.route('/health', methods=['GET'])
def health():
	return jsonify({'estado': 'saludable'}), 200
