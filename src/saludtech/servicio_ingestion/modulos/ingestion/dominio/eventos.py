from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.servicio_ingestion.seedwork.dominio.eventos import (EventoDominio)
import saludtech.servicio_ingestion.modulos.ingestion.dominio.objetos_valor as ov
from datetime import datetime

@dataclass
class ProcesoIngestionCreado(EventoDominio):
    id_proceso_ingestion: uuid.UUID = None
    id_partner: uuid.UUID = None
    fecha_creacion: datetime = None
    imagenes: list[ov.Imagen] = None