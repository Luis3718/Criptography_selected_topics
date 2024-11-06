from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class NivelesEstudios(Base):
    __tablename__ = "NivelesEstudios"
    ID_NivelEstudios = Column(Integer, primary_key=True)
    NivelEstudios = Column(String(100), nullable=False)

class Ocupaciones(Base):
    __tablename__ = "Ocupaciones"
    ID_Ocupacion = Column(Integer, primary_key=True)
    Ocupacion = Column(String(100), nullable=False)

class Residencias(Base):
    __tablename__ = "Residencias"
    ID_Residencia = Column(Integer, primary_key=True)
    Residencia = Column(String(100), nullable=False)

class EstadoCivil(Base):
    __tablename__ = "EstadoCivil"
    ID_EstadoCivil = Column(Integer, primary_key=True)
    Estado = Column(String(50), nullable=False)

# Definir la tabla Pacientes
class Pacientes(Base):
    __tablename__ = "Pacientes"
    ID_Paciente = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    Correo = Column(String(255), unique=True, nullable=False)
    Contraseña = Column(String(255), nullable=False)
    Sexo = Column(Enum('Mujer', 'Hombre', 'Prefiero no decirlo'), nullable=False)
    Edad = Column(Integer, nullable=False)
    ID_NivelEstudios = Column(Integer, ForeignKey("NivelesEstudios.ID_NivelEstudios"))
    ID_Ocupacion = Column(Integer, ForeignKey("Ocupaciones.ID_Ocupacion"))
    ID_Residencia = Column(Integer, ForeignKey("Residencias.ID_Residencia"))
    ID_EstadoCivil = Column(Integer, ForeignKey("EstadoCivil.ID_EstadoCivil"))
    EnTratamiento = Column(Boolean, nullable=False)
    TomaMedicamentos = Column(Enum('Sí', 'No', 'No aplica'), nullable=False)
    nombre_medicacion = Column(String(255))