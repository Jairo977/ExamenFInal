# Configuración del microservicio inventario
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
	MYSQL_USER = os.getenv('MYSQL_USER', 'user')
	MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
	MYSQL_DB = os.getenv('MYSQL_DB', 'inventory_db')
	RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
