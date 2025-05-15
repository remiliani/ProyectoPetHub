from .database import engine, SessionLocal, Base
from .models import Cliente
from sqlalchemy.orm import Session

def create_superuser():
    Base.metadata.create_all(bind=engine)  # Asegura que las tablas existen

    db: Session = SessionLocal()
    try:
        # Verificar si ya existe un admin (opcional)
        admin_exists = db.query(Cliente).filter(Cliente.is_admin == True).first()
        if admin_exists:
            print("Superusuario ya existe.")
            return

        # Crear superusuario
        superuser = Cliente(
            nombre='supervisoradmin',
            email='supervisoradmin@example.com',
            password='adminpass1234',  # Ideal: hashea la contraseña, aquí para ejemplo simple
            is_admin=True,
            soft_deleted=False
        )
        db.add(superuser)
        db.commit()
        print("Superusuario creado correctamente.")
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser()
