from enum import Enum

class Roles(str, Enum):
    SUPERADMIN = "Super Administrador"
    ADMIN = "Administrador"
    ENTRENADOR = "Entrenador"
    CLIENTE = "Cliente"
    