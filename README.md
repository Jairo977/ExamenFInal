
# Examen Final - Microservicios con Kubernetes y Docker

Este proyecto implementa una arquitectura de microservicios para un sistema de gestión agrícola, incluyendo los servicios de **central-core**, **inventario** y **facturación**, orquestados con Kubernetes y Docker. Incluye integración con bases de datos (PostgreSQL, MySQL, MariaDB) y mensajería con RabbitMQ.

## Estructura del Proyecto

| Carpeta/Archivo      | Descripción                                                      |
|----------------------|------------------------------------------------------------------|
| central-core/        | Servicio principal (Flask + PostgreSQL)                          |
| inventario/          | Microservicio de inventario (Flask + MySQL)                      |
| facturacion/         | Microservicio de facturación (Flask + MariaDB)                   |
| k8s/                 | Archivos YAML para despliegue en Kubernetes                      |
| .github/             | Instrucciones y flujos de trabajo                                |
| README.md            | Este archivo                                                    |

## Tecnologías Utilizadas

- Python 3 (Flask)
- Docker
- Kubernetes
- PostgreSQL, MySQL, MariaDB
- RabbitMQ

## Despliegue Local con Docker

1. Construye las imágenes de cada microservicio:
	```sh
	docker build -t tuusuario/central-core ./central-core
	docker build -t tuusuario/inventario ./inventario
	docker build -t tuusuario/facturacion ./facturacion
	```
2. Lanza los contenedores de bases de datos y RabbitMQ:
	```sh
	docker run -d --name postgres -e POSTGRES_DB=central_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
	docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=inventory_db -e MYSQL_USER=user -e MYSQL_PASSWORD=password -p 3306:3306 mysql:8
	docker run -d --name mariadb -e MARIADB_ROOT_PASSWORD=password -e MARIADB_DATABASE=billing_db -e MARIADB_USER=user -e MARIADB_PASSWORD=password -p 3307:3306 mariadb:11
	docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
	```
3. Lanza los microservicios:
	```sh
	docker run -d --name central-core --link postgres -p 5000:5000 tuusuario/central-core
	docker run -d --name inventario --link mysql -p 5001:5001 tuusuario/inventario
	docker run -d --name facturacion --link mariadb -p 5002:5002 tuusuario/facturacion
	```

## Despliegue en Kubernetes

1. Aplica los recursos:
	```sh
	kubectl apply -f k8s/
	```
2. Verifica los pods y servicios:
	```sh
	kubectl get pods
	kubectl get svc
	```
3. (Opcional) Expón los servicios con Ingress o NodePort según tu entorno.

## Variables de Entorno

Las variables de entorno se gestionan mediante ConfigMaps y Secrets en Kubernetes. Consulta los archivos en `k8s/` para detalles.

## Pruebas y Flujo de Facturación

- El microservicio de facturación consume eventos de RabbitMQ y genera facturas automáticamente.
- Puedes probar el flujo publicando eventos con el script `publicar_evento.py`.

## Autor

- Jairo977
- [Repositorio en GitHub](https://github.com/Jairo977/ExamenFInal)

---

> Proyecto para examen final. Arquitectura robusta, escalable y lista para producción en contenedores y Kubernetes.
