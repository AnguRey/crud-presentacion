from database import Base, engine
from models import Tarea

# Crear las tablas en la base de datos
print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
