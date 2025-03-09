from dataclasses import dataclass, field
from saludtech.servicio_anonimizacion.seedwork.aplicacion.dto import DTO

@dataclass()
class DatoDTO(DTO):
    tipo: str
    contenido: str
    anonimizado: bool = field(default_factory=bool)

@dataclass()
class ProcesoAnonimizacionDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    datos: list[DatoDTO] = field(default_factory=list)
    id_partner: str = field(default_factory=str)