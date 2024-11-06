from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr

class PacienteLogin(BaseModel):
    Correo: EmailStr
    Contraseña: str

class PacienteLoginResponse(BaseModel):
    ID_Paciente: int
    Nombre: str
    Correo: EmailStr
    token: str  # Asegúrate de que este campo esté incluido
    Mensaje: str
    
class PacienteCreate(BaseModel):
    Nombre: str
    Correo: EmailStr
    Contraseña: str
    Sexo: Literal['Mujer', 'Hombre', 'Prefiero no decirlo']
    Edad: int
    ID_NivelEstudios: int
    ID_Ocupacion: int
    ID_Residencia: int
    ID_EstadoCivil: int
    EnTratamiento: bool
    TomaMedicamentos: Literal['Sí', 'No', 'No aplica']
    nombre_medicacion: Optional[str]

class PacienteResponse(BaseModel):
    ID_Paciente: int
    Nombre: str
    Correo: EmailStr
    Sexo: Literal['Mujer', 'Hombre', 'Prefiero no decirlo']
    Edad: int
    ID_NivelEstudios: int
    ID_Ocupacion: int
    ID_Residencia: int
    ID_EstadoCivil: int
    EnTratamiento: bool
    TomaMedicamentos: Literal['Sí', 'No', 'No aplica']
    nombre_medicacion: Optional[str]
