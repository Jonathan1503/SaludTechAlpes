from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.servicio_anonimizacion.seedwork.dominio.eventos import (EventoDominio)
import saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.objetos_valor as ov
from datetime import datetime
import uuid

class EventoAnonimizacion(EventoDominio):
    ...

@dataclass
class ProcesoAnonimizacionCreado(EventoAnonimizacion):
    id_proceso_anonimizacion: uuid.UUID = None
    id_proceso_original: uuid.UUID = None
    id_correlacion: str = None
    fecha_creacion: datetime = None
    imagenes: list[ov.ImagenAnonimizada] = None

@dataclass
class CreacionProcesoAnonimizacionFallido(EventoAnonimizacion):
    id_proceso_anonimizacion: uuid.UUID = None
    id_proceso_original: uuid.UUID = None
    id_correlacion: str = None
    fecha_creacion: datetime = None
    imagenes: list[ov.ImagenAnonimizada] = None