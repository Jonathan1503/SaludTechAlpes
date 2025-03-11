from saludtech.servicio_ingestion.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass, field
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.dto import ImagenEstandarizadaDTO
@dataclass
class ProcesarEstandarizacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    imagenes: list[ImagenEstandarizadaDTO]
    id_proceso_ingestion: str
    estado: str

class CancelarProcesoEstandarizacion(Comando):
    ...
