# Configuración del microservicio facturación
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	MYSQL_HOST = os.getenv('MARIA_HOST', 'mariadb')
	MYSQL_USER = os.getenv('MARIA_USER', 'user')
	MYSQL_PASSWORD = os.getenv('MARIA_PASSWORD', 'password')
	MYSQL_DB = os.getenv('MARIA_DB', 'billing_db')
	RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
	CENTRAL_API = os.getenv('CENTRAL_API', 'http://central-core:5000')
