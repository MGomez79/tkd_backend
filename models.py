from sqlalchemy import Column, String, Integer
from db import Base, engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer,autoincrement=True , primary_key=True)
    username = Column(String(70),unique=True)
    #last_name = Column(String(70),unique=True)
    email = Column(String(70),unique=True)
    password = Column(String(200))
    deportista = relationship('Deportista', backref="usuario")

class Deportista(Base):
    __tablename__= 'deportista'
    id_documento = Column(Integer, primary_key=True)
    categoria = Column(String(30),unique=True)
    peso = Column(String(20),unique=True)
    edad = Column(Integer)
    estatura = Column(String(70),unique=True)
    username_id = Column(Integer, ForeignKey("usuario.id"))
    experiencia = Column(Integer)
    #username_id = Column(Integer)
    #venta = Column(Integer)
    
#Base.metadata.create_all(engine)