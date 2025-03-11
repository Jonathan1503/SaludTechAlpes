from saludtech.servicio_ingestion.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass, field
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.dto import ImagenAnonimizadaDTO
@dataclass
class AnonimizarProceso(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    imagenes: list[ImagenAnonimizadaDTO]
    id_proceso_original: str
class CancelarProcesoAnonimizacion(Comando):
    ...

