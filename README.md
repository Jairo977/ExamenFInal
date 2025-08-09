# Evaluación Conjunta - Microservicios Flask, Docker y Kubernetes

Este proyecto resuelve la evaluación conjunta implementando una arquitectura de microservicios con Flask, Docker y Kubernetes.

## Estructura del Proyecto

```
Examen/
├── central-core/         # Microservicio de gestión de agricultores y cosechas (Flask + PostgreSQL)
├── inventario/           # Microservicio de inventario de insumos (Flask + MySQL)
├── facturacion/          # Microservicio de facturación (Flask + MariaDB)
├── k8s/                  # Archivos de despliegue para Kubernetes
├── broker/               # Configuración de RabbitMQ (si aplica)
├── .github/              # Instrucciones y flujos de trabajo
└── README.md
```

## Endpoints Principales

### Central-Core
- CRUD Agricultores: `/agricultores` (GET, POST, PUT, DELETE)
- CRUD Cosechas: `/cosechas` (GET, POST, PUT, DELETE)
- Actualizar estado: `/cosechas/<id>` (PUT)

### Inventario
- CRUD Insumos: `/insumos` (GET, POST, PUT, DELETE)

### Facturación
- CRUD Facturas: `/facturas` (GET, POST, PUT, DELETE)

### Salud
- Todos los servicios: `/health` (GET)

## ¿Cómo ejecutar localmente?

1. Clona el repositorio y entra a la carpeta de cada microservicio.
2. Crea un entorno virtual y activa:
	```sh
	python -m venv .venv
	source .venv/bin/activate  # Linux/Mac
	.venv\Scripts\activate    # Windows
	```
3. Instala dependencias:
	```sh
	pip install -r requirements.txt
	```
4. Configura las variables de entorno necesarias (puedes usar un archivo `.env`).
5. Ejecuta el microservicio:
	```sh
	flask --app app run --host=0.0.0.0 --port=5000  # Cambia el puerto según el microservicio
	```

## Uso con Docker

1. Construye la imagen Docker:
	```sh
	docker build -t tuusuario/central-core:latest .
	```
2. Ejecuta el contenedor:
	```sh
	docker run -p 5000:5000 --env-file .env tuusuario/central-core:latest
	```
3. Repite para cada microservicio cambiando el nombre y el puerto.

## Despliegue en Kubernetes

1. Personaliza los archivos en la carpeta `k8s/` según tus imágenes y credenciales.
2. Aplica los recursos:
	```sh
	kubectl apply -f k8s/
	```
3. Verifica los pods y servicios:
	```sh
	kubectl get pods
	kubectl get svc
	```

## Notas
- Cada microservicio tiene su propia base de datos y no comparte datos directamente.
- La comunicación entre microservicios se realiza mediante RabbitMQ.
- Los archivos de configuración usan variables de entorno para facilitar el despliegue en diferentes entornos.

## Créditos y Licencia
Desarrollado para la Evaluación Conjunta 2025. Puedes modificar y reutilizar este proyecto según tus necesidades académicas.
