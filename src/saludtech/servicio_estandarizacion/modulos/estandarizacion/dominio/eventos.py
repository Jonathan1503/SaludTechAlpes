from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.servicio_estandarizacion.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class ProcesoEstandarizacionCreado(EventoDominio):
    id_proceso_estandarizacion: uuid.UUID = None
    id_proceso_ingestion: uuid.UUID = None
    fecha_creacion: datetime = None

@dataclass
class ProcesoEstandarizacionCompletado(EventoDominio):
    id_proceso_estandarizacion: uuid.UUID = None
    id_proceso_ingestion: uuid.UUID = None
    fecha_actualizacion: datetime = None