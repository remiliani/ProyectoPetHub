import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# Cargar variables de entorno desde el archivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Crear la URL de conexión para MySQL
DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear motor SQLAlchemy para conectar con la base de datos MySQL
engine = create_engine(DATABASE_URL, echo=True)

# Clase base para declarar los modelos
Base = declarative_base()

# Crear todas las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear clase Session para manejar conexiones/consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función de utilidad para obtener la sesión y manejarla
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

