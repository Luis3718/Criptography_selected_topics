from sqlalchemy.orm import Session
from models import Pacientes
from schemas import PacienteCreate
from passlib.context import CryptContext

# Crear contexto para manejar hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_credenciales(db: Session, correo: str, contraseña: str):
    paciente = db.query(Pacientes).filter(Pacientes.Correo == correo).first()
    if not paciente:
        return None
    if not pwd_context.verify(contraseña, paciente.Contraseña):  # Confirmación de contraseña
        return None
    return paciente

def crear_paciente(db: Session, paciente: PacienteCreate):
    hashed_password = pwd_context.hash(paciente.Contraseña)
    nuevo_paciente = Pacientes(
        Nombre=paciente.Nombre,
        Correo=paciente.Correo,
        Contraseña=hashed_password,  # Usar la contraseña cifrada
        Sexo=paciente.Sexo,
        Edad=paciente.Edad,
        ID_NivelEstudios=paciente.ID_NivelEstudios,
        ID_Ocupacion=paciente.ID_Ocupacion,
        ID_Residencia=paciente.ID_Residencia,
        ID_EstadoCivil=paciente.ID_EstadoCivil,
        EnTratamiento=paciente.EnTratamiento,
        TomaMedicamentos=paciente.TomaMedicamentos,
        nombre_medicacion=paciente.nombre_medicacion
    )
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return nuevo_paciente