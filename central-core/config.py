# Configuración del microservicio central
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg2://user:password@postgres:5432/central_db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
