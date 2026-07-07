import uvicorn
from app.models.seed import seed_database
import os


def inicializar():
    db_path = os.path.join(os.path.dirname(__file__), "retailnova.db")
    if not os.path.exists(db_path):
        print("Base de datos no encontrada. Creando...")
        seed_database()
    else:
        print("Base de datos encontrada.")


if __name__ == "__main__":
    inicializar()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
