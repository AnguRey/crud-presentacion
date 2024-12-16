import os
import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Tarea
import json


# Crear una sesión para interactuar con la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
    finally:
        db.close()

# Función para listar las tareas
def listar_tareas(db):
    try:
        return db.query(Tarea).all()
    except Exception as e:
        st.error(f"Error al listar tareas: {e}")
        return []

# Función para agregar una nueva tarea
def agregar_tarea(db, titulo, descripcion):
    try:
        nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
        db.add(nueva_tarea)
        db.commit()
        db.refresh(nueva_tarea)
        return nueva_tarea
    except Exception as e:
        db.rollback()
        st.error(f"Error al agregar tarea: {e}")

# Función para eliminar tareas completadas
def eliminar_completadas(db):
    try:
        db.query(Tarea).filter(Tarea.estado == "completada").delete()
        db.commit()
    except Exception as e:
        db.rollback()
        st.error(f"Error al eliminar tareas: {e}")

# Función para actualizar el estado de la tarea (completar/pendiente)
def actualizar_estado_tarea(db, tarea_id, estado):
    try:
        tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
        if tarea:
            tarea.estado = estado
            db.commit()
            db.refresh(tarea)
            return True  # Indica éxito
        else:
            st.warning("Tarea no encontrada.")
            return False
    except Exception as e:
        db.rollback()
        st.error(f"Error al actualizar el estado de la tarea: {e}")
        return False


def main():
    st.set_page_config(page_title="Gestión de Tareas", page_icon="✅", layout="wide")
    st.markdown("<h2 style='text-align: center;'>📝 Gestión de Tareas</h2>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center;'>IMPORTANTE: Las actulizaciones se ven reflejadas cuando ocurre una actulizacion en la pagina(EXPORTAR-IMPORTAR-ELIMINAR)</h4>", unsafe_allow_html=True)

    # Crear contenedores para las secciones
    agregar_col, lista_col, admin_col = st.columns([1, 1, 1])

    with agregar_col:
        st.markdown("<h2 style='text-align: center;'>➕ Agregar Tarea</h2>", unsafe_allow_html=True)
        titulo = st.text_input("Título de la tarea")
        descripcion = st.text_area("Descripción de la tarea")
        if st.button("Agregar Tarea"):
            if titulo.strip():
                db = next(get_db())
                agregar_tarea(db, titulo, descripcion)
                db.close()
                st.success("Tarea agregada con éxito.")
            else:
                st.error("El título de la tarea no puede estar vacío.")

    with lista_col:
        st.markdown("<h2 style='text-align: center;'>📋 Lista de Tareas</h2>", unsafe_allow_html=True)
        db = next(get_db())
        tareas = listar_tareas(db)
        db.close()

        if tareas:
            for idx, tarea in enumerate(tareas):
                with st.expander(f"📌 {tarea.titulo} ({tarea.estado})"):
                    st.write(f"**Descripción:** {tarea.descripcion or 'Sin descripción'}")
                    nueva_estado = "pendiente" if tarea.estado == "completada" else "completada"
                    accion = "Marcar como completada" if tarea.estado == "pendiente" else "Desmarcar"

                    # Botón para cambiar el estado
                    if st.button(accion, key=f"boton_{idx}"):
                        db = next(get_db())
                        if actualizar_estado_tarea(db, tarea.id, nueva_estado):
                            db.close()
                            # Actualizar localmente el estado
                            tarea.estado = nueva_estado
                        else:
                            db.close()
        else:
            st.info("No hay tareas registradas.")

    with admin_col:
        st.markdown("<h2 style='text-align: center;'>⚙️ Administración</h2>", unsafe_allow_html=True)
        
        # Manejo de excepciones al eliminar tareas completadas
        if st.button("Eliminar Tareas Completadas"):
            try:
                db = next(get_db())

                # Filtrar las tareas completadas directamente
                tareas_completadas = db.query(Tarea).filter(Tarea.estado == "completada").all()
                
                # Validar si hay tareas completadas
                if not tareas_completadas:
                    st.warning("No hay tareas completadas para eliminar.")
                else:
                    eliminar_completadas(db)  # Lógica de eliminación
                    st.success("Tareas completadas eliminadas.")
            except ConnectionError:
                st.error("Error de conexión con la base de datos.")
            except PermissionError:
                st.error("No tienes permisos para modificar las tareas.")
            except Exception as e:
                st.error(f"Error inesperado: {e}")
            finally:
                db.close()  # Cierra la conexión a la base de datos


        archivo = st.text_input("Archivo (ejemplo: tareas.json)")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Exportar Tareas"):
                if archivo.strip():
                    db = next(get_db())
                    exportar_tareas(db, archivo)
                    db.close()
                else:
                    st.error("Debes especificar un nombre de archivo.")
        with col2:
            if st.button("Importar Tareas"):
                if archivo.strip():
                    db = next(get_db())
                    importar_tareas(db, archivo)
                    db.close()
                else:
                    st.error("Debes especificar un nombre de archivo.")

def exportar_tareas(db, archivo):
    try:
        # Validar que la lista de tareas no esté vacía
        tareas = listar_tareas(db)
        if not tareas:
            st.warning("No hay tareas para exportar.")
            return

        # Validar que el archivo tenga una extensión válida
        if not archivo.endswith(".json"):
            st.error("El archivo debe tener la extensión .json.")
            return

        # Crear la estructura de datos para exportar
        datos = [
            {"titulo": tarea.titulo, "descripcion": tarea.descripcion, "estado": tarea.estado}
            for tarea in tareas
        ]

        # Intentar escribir en el archivo
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        st.success(f"Tareas exportadas a {archivo}")
    except FileNotFoundError:
        st.error("No se encontró la ruta o el archivo especificado.")
    except PermissionError:
        st.error("No tienes permisos para escribir en este archivo o directorio.")
    except json.JSONDecodeError:
        st.error("Hubo un problema al procesar los datos en formato JSON.")
    except Exception as e:
        st.error(f"Error inesperado al exportar tareas: {e}")

def importar_tareas(db, archivo):
    if not archivo:  # Verifica si el archivo está vacío o no se seleccionó
        st.error("No se ha seleccionado ningún archivo para importar.")
        return

    # Validar que el archivo tenga una extensión válida
    if not archivo.endswith(".json"):
        st.error("El archivo debe tener la extensión .json.")
        return

    if not os.path.exists(archivo):  # Verifica si el archivo existe
        st.error(f"El archivo '{archivo}' no existe.")
        return

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        if not datos:  # Verifica si el archivo está vacío
            st.warning("El archivo está vacío. No se importaron tareas.")
            return

        for tarea in datos:
            nueva_tarea = Tarea(
                titulo=tarea["titulo"],
                descripcion=tarea["descripcion"],
                estado=tarea["estado"]
            )
            db.add(nueva_tarea)
        
        db.commit()
        st.success(f"Tareas importadas exitosamente desde {archivo}")
    except json.JSONDecodeError:
        st.error(f"El archivo '{archivo}' no tiene un formato JSON válido.")
    except KeyError as e:
        st.error(f"Falta una clave necesaria en el archivo JSON: {e}")
    except Exception as e:
        db.rollback()
        st.error(f"Error al importar tareas: {e}")

if __name__ == "__main__":
    main()
