from sqlalchemy import Column, Integer, String
from database import Base

# Modelo para la tabla "tareas"
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(String, nullable=False, default="pendiente")
