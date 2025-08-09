# Rutas y lógica del microservicio central
from flask import Blueprint, request, jsonify
from uuid import uuid4
import pika
import json
from .modelos import db, Agricultor, Cosecha
from config import Config

bp = Blueprint('central', __name__)

# CRUD Agricultores
@bp.route('/agricultores', methods=['POST'])
def crear_agricultor():
	data = request.get_json()
	agricultor = Agricultor(
		agricultor_id=str(uuid4()),
		nombre=data['nombre'],
		finca=data['finca'],
		ubicacion=data['ubicacion'],
		correo=data['correo']
	)
	db.session.add(agricultor)
	db.session.commit()
	return jsonify({'agricultor_id': agricultor.agricultor_id}), 201

@bp.route('/agricultores', methods=['GET'])
def listar_agricultores():
	agricultores = Agricultor.query.all()
	return jsonify([
		{
			'agricultor_id': a.agricultor_id,
			'nombre': a.nombre,
			'finca': a.finca,
			'ubicacion': a.ubicacion,
			'correo': a.correo,
			'fecha_registro': a.fecha_registro.isoformat() if a.fecha_registro else None
		} for a in agricultores
	])

@bp.route('/agricultores/<agricultor_id>', methods=['PUT'])
def actualizar_agricultor(agricultor_id):
	agricultor = Agricultor.query.get(agricultor_id)
	if not agricultor:
		return jsonify({'error': 'Agricultor no encontrado'}), 404
	data = request.get_json()
	agricultor.nombre = data.get('nombre', agricultor.nombre)
	agricultor.finca = data.get('finca', agricultor.finca)
	agricultor.ubicacion = data.get('ubicacion', agricultor.ubicacion)
	agricultor.correo = data.get('correo', agricultor.correo)
	db.session.commit()
	return jsonify({'mensaje': 'Agricultor actualizado'})

@bp.route('/agricultores/<agricultor_id>', methods=['DELETE'])
def eliminar_agricultor(agricultor_id):
	agricultor = Agricultor.query.get(agricultor_id)
	if not agricultor:
		return jsonify({'error': 'Agricultor no encontrado'}), 404
	db.session.delete(agricultor)
	db.session.commit()
	return jsonify({'mensaje': 'Agricultor eliminado'})

# CRUD Cosechas
@bp.route('/cosechas', methods=['POST'])
def crear_cosecha():
	data = request.get_json()
	if not Agricultor.query.get(data['agricultor_id']):
		return jsonify({'error': 'Agricultor no encontrado'}), 404
	if data['toneladas'] <= 0:
		return jsonify({'error': 'Cantidad inválida'}), 400
	cosecha_id = str(uuid4())
	cosecha = Cosecha(
		cosecha_id=cosecha_id,
		agricultor_id=data['agricultor_id'],
		producto=data['producto'],
		toneladas=data['toneladas']
	)
	db.session.add(cosecha)
	db.session.commit()
	# Publicar evento en RabbitMQ
	try:
		connection = pika.BlockingConnection(pika.URLParameters(Config.RABBITMQ_URL))
		channel = connection.channel()
		channel.exchange_declare(exchange='cosechas', exchange_type='topic')
		mensaje = {
			'event_id': str(uuid4()),
			'event_type': 'nueva_cosecha',
			'payload': {
				'cosecha_id': cosecha_id,
				'producto': data['producto'],
				'toneladas': data['toneladas'],
				'requiere_insumos': ['Semilla ' + data['producto'], 'Fertilizante N-PK']
			}
		}
		channel.basic_publish(exchange='cosechas', routing_key='nueva', body=json.dumps(mensaje))
		connection.close()
	except Exception as e:
		print('Error publicando en RabbitMQ:', e)
	return jsonify({'cosecha_id': cosecha_id}), 201

@bp.route('/cosechas', methods=['GET'])
def listar_cosechas():
	cosechas = Cosecha.query.all()
	return jsonify([
		{
			'cosecha_id': c.cosecha_id,
			'agricultor_id': c.agricultor_id,
			'producto': c.producto,
			'toneladas': c.toneladas,
			'estado': c.estado,
			'creado_en': c.creado_en.isoformat() if c.creado_en else None,
			'factura_id': c.factura_id
		} for c in cosechas
	])

@bp.route('/cosechas/<cosecha_id>', methods=['PUT'])
def actualizar_cosecha(cosecha_id):
	cosecha = Cosecha.query.get(cosecha_id)
	if not cosecha:
		return jsonify({'error': 'Cosecha no encontrada'}), 404
	data = request.get_json()
	cosecha.producto = data.get('producto', cosecha.producto)
	cosecha.toneladas = data.get('toneladas', cosecha.toneladas)
	cosecha.estado = data.get('estado', cosecha.estado)
	cosecha.factura_id = data.get('factura_id', cosecha.factura_id)
	db.session.commit()
	return jsonify({'mensaje': 'Cosecha actualizada'})

@bp.route('/cosechas/<cosecha_id>', methods=['DELETE'])
def eliminar_cosecha(cosecha_id):
	cosecha = Cosecha.query.get(cosecha_id)
	if not cosecha:
		return jsonify({'error': 'Cosecha no encontrada'}), 404
	db.session.delete(cosecha)
	db.session.commit()
	return jsonify({'mensaje': 'Cosecha eliminada'})

# Endpoint de salud
@bp.route('/health', methods=['GET'])
def health():
	return jsonify({'estado': 'saludable'}), 200
