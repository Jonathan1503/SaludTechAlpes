from dataclasses import dataclass, field
from saludtech.servicio_estandarizacion.seedwork.aplicacion.dto import DTO

@dataclass()
class ImagenEstandarizadaDTO(DTO):
    tipo: str
    archivo: str

@dataclass()
class ProcesoEstandarizacionDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    imagenes: list[ImagenEstandarizadaDTO] = field(default_factory=list)
    id_proceso_ingestion: str = field(default_factory=str)
    estado: str = field(default_factory=str)
