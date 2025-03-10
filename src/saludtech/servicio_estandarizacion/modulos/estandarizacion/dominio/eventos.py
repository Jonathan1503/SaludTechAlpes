from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.servicio_estandarizacion.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoEstandarizacion(EventoDominio):
    ...

@dataclass
class ProcesoEstandarizacionCreado(EventoEstandarizacion):
    id_proceso_estandarizacion: uuid.UUID = None
    id_proceso_ingestion: uuid.UUID = None
    id_correlacion: str = None
    fecha_creacion: datetime = None

@dataclass
class CreacionProcesoEstandarizacionFallido(EventoEstandarizacion):
    id_proceso_estandarizacion: uuid.UUID = None
    id_proceso_ingestion: uuid.UUID = None
    id_correlacion: str = None
    fecha_creacion: datetime = None

@dataclass
class ProcesoEstandarizacionCompletado(EventoEstandarizacion):
    id_proceso_estandarizacion: uuid.UUID = None
    id_proceso_ingestion: uuid.UUID = None
    fecha_actualizacion: datetime = None