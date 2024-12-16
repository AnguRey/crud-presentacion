from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Configurar la conexión a SQLite
DATABASE_URL = "sqlite:///tareas.db"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
Base = declarative_base()
