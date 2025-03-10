from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.servicio_ingestion.seedwork.dominio.eventos import (EventoDominio)
import saludtech.servicio_ingestion.modulos.ingestion.dominio.objetos_valor as ov
from datetime import datetime

class EventoIngestion(EventoDominio):
    ...


@dataclass
class ProcesoIngestionCreado(EventoIngestion):
    id_proceso_ingestion: uuid.UUID = None
    id_partner: uuid.UUID = None
    id_correlacion: str = None
    fecha_creacion: datetime = None
    imagenes: list[ov.Imagen] = None
@dataclass
class CreacionProcesoIngestionFallido(EventoIngestion):
    id_proceso_ingestion: uuid.UUID = None
    id_partner: uuid.UUID = None
    id_correlacion: str = None
    fecha_creacion: datetime = None
    imagenes: list[ov.Imagen] = None