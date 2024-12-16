Aplicación de Manejador de Tareas

Descripción

Esta es una aplicación de gestion tareas. Ofrece una interfaz creada con Streamlit para agregar, listar, completar, eliminar , exportar y exportar.

Tecnologías Utilizadas

Front-end: Streamlit
Back-end: Python
Base de datos: SQLAlchemy (SQLite)
Escaneo de calidad del código: SonarQube

Funcionalidades

Agregar Tareas:
Permite al usuario agregar nuevas tareas con un título y una descripción.

Listar Tareas:
Muestra todas las tareas registradas, indicando su estado (pendiente o completada).

Marcar Tareas como Completadas:
Cambia el estado de una tarea de "pendiente" a "completada" o viceversa.

Eliminar Tareas Completadas:
Permite eliminar todas las tareas marcadas como completadas.

Exportar e Importar Tareas:
Ofrece la posibilidad de guardar las tareas en un archivo JSON y cargarlas desde el mismo archivo.

Requisitos Técnicos

Uso de listas y diccionarios para gestionar las tareas temporalmente.

Manejo de excepciones para prevenir cierres inesperados de la aplicación.

Módulos de Python utilizados:

json para la exportación e importación de tareas.
os para verificar rutas de archivos.

SQLAlchemy como ORM para la gestión de la base de datos.Streamlit para la creación de una interfaz gráfica simple e interactiva.

Configuración e Instalación

Prerrequisitos

Python 3.10 o superior.
Virtualenv para gestionar dependencias.

Instalación

1.Clona este repositorio:

git clone https://github.com/tu-usuario/crud-presentacion.git

2.Ve al directorio del proyecto:

    cd crud-presentacion
    
3.Crea un entorno virtual e instala las dependencias:

    python -m venv venv
    
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    
    pip install -r requirements.txt
    
4.Crea la base de datos:

    python setup_db.py
    
5.Ejecuta la aplicación:

    streamlit run app.py

Configuración de SonarQube

1.Configura un servidor SonarQube y asegúrate de tener un token de acceso.

2.Configura el archivo sonar-project.properties con los detalles de tu proyecto.

3.Ejecuta el análisis desde la terminal:

    sonar-scanner

Uso de la Aplicación

Accede a la aplicación desde tu navegador:

  ![image](https://github.com/user-attachments/assets/738dc469-e76a-4439-8657-d452571ffc16)

  http://localhost:8501
  
  ![image](https://github.com/user-attachments/assets/9b9f2947-7ef4-4c86-a686-68e0bd684815)

Capturas de Pantalla

Interfaz de Inicio: 

![image](https://github.com/user-attachments/assets/687ae1c8-6486-497f-b18a-76896b623a4a)

Agregar Tareas: 

![image](https://github.com/user-attachments/assets/06f7fedc-49fa-42b4-97f9-4167cd43e814)

Lista de Tareas: 

![image](https://github.com/user-attachments/assets/eb94cefb-9bbb-4aae-9284-ad9fbac7d9d2)

Administración eliminar: 

![image](https://github.com/user-attachments/assets/525c9b37-3c69-4c80-a8ba-38dd3f902b8e)

![image](https://github.com/user-attachments/assets/04e3f6cb-3012-4f6b-8e51-e31b0d01af80)

Exportar: ![image](https://github.com/user-attachments/assets/fcea312f-35d6-42b7-9a50-783662e44213)

Importar: ![image](https://github.com/user-attachments/assets/c0bf63c3-4dcf-4817-9185-33e5948392e7)

Contribuciones

Las contribuciones son bienvenidas. Por favor, correcciones o nuevas funcionalidades.








