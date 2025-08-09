import pika
import json

rabbit_url = "amqp://guest:guest@localhost:5672/"
cosecha_id = "AQUI_PON_EL_ID_DE_LA_COSECHA"  # Reemplaza por el cosecha_id real

connection = pika.BlockingConnection(pika.URLParameters(rabbit_url))
channel = connection.channel()
channel.queue_declare(queue='cola_facturacion')

mensaje = {"cosecha_id": cosecha_id}
channel.basic_publish(
    exchange='',
    routing_key='cola_facturacion',
    body=json.dumps(mensaje)
)

print("Mensaje enviado:", mensaje)
connection.close()
