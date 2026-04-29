# 🗳️ Voting API

API REST desarrollada con **FastAPI** para gestionar un sistema básico de votaciones y obtener estadísticas de los resultados.

---

## 🚀 Tecnologías utilizadas

- Python 3
- FastAPI
- Uvicorn
- SQLite

---

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/Andresleo9/voting-api.git
cd voting-api
```
#Crea un entorno virtual

python -m venv venv
venv\Scripts\activate   # Windows

#Instala dependencias:
pip install fastapi uvicorn

#Inicia el servidor con:
uvicorn main:app --reload

#FastAPI genera documentación automática:

Swagger UI: http://127.0.0.1:8000/docs

#estructura del proyecto:
Prueba/
│── main.py
│── models.py
│── schemas.py
│── crud.py
│── database.py
│── voting.db

## 📊 Capturas

### Swagger UI
![Swagger](images/swagger.png)

### Estadísticas
![Statistics](images/statistics.png)

## 👨‍💻 Autor

Andresleo9

