# Práctica Docker – GitHub Codespaces

Aplicación web para registrar productos (nombre, categoría y precio) y guardarlos en MySQL (`mydb`). Se construye, ejecuta y publica como imagen Docker llamada `examen`.

## Requisitos

- GitHub Codespaces (recomendado) o Docker Desktop
- Cuenta en [Docker Hub](https://hub.docker.com/)

## Conexión a MySQL

El archivo `db.py` conecta con la base **mydb**:

| Variable | Valor por defecto |
|---|---|
| `DB_HOST` | `localhost` (en Compose: `db`) |
| `DB_PORT` | `3306` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | `root` |
| `DB_NAME` | `mydb` |

`init.sql` crea la base `mydb` y la tabla `productos`.

## 1. Subir el proyecto a GitHub

```bash
git add .
git commit -m "Practica Docker: registro de productos con MySQL"
git push
```

Luego abre el repositorio en GitHub y crea un Codespace.

## 2. Crear la imagen `examen`

```bash
docker build -t examen .
```

## 3. Crear la base de datos y ejecutar la aplicación

Con Compose se levantan MySQL (`mydb`) y la app:

```bash
docker compose up -d --build
```

Abre `http://localhost:8080` (en Codespaces usa el puerto 8080 publicado).

## 4. Subir la imagen a Docker Hub

Reemplaza `TU_USUARIO` por tu usuario de Docker Hub:

```bash
docker login
docker tag examen TU_USUARIO/examen
docker push TU_USUARIO/examen
```

## 5. Ejecutar desde Docker Hub

La app necesita MySQL. Lo más simple es usar Compose (la imagen web se llama `examen`).

```bash
docker compose up -d
```

## API

- `GET /api/productos` — lista productos
- `POST /api/productos` — guarda un producto

```json
{ "nombre": "Teclado", "categoria": "Periféricos", "precio": 25.5 }
```
