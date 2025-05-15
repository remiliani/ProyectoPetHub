from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = 'cliente'   
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String, unique=True )
    password = Column(String)
    is_admin = Column(Integer, default=0)
    soft_delete = Column(Boolean, default=False)
    mascotas = relationship("Mascota", back_populates="cliente")

class Mascota(Base):
    __tablename__ = 'mascota'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    especie = Column(String)
    edad = Column(Integer)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    soft_delete = Column(Boolean, default=False)
    cliente = relationship("Cliente", back_populates="mascotas")
    citas = relationship("Cita", back_populates="mascota")

class Cita(Base):
    __tablename__ = 'cita'
    
    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    motivo = Column(String)
    mascota_id = Column(Integer, ForeignKey('mascota.id'))
    soft_delete = Column(Boolean, default=False)
    mascota = relationship("Mascota", back_populates="citas")
