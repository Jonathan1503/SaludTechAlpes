from __future__ import annotations
from dataclasses import dataclass, field
from saludtech.servicio_anonimizacion.seedwork.dominio.eventos import (EventoDominio)
import saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.objetos_valor as ov
from datetime import datetime
import uuid

@dataclass
class ProcesoAnonimizacionCreado(EventoDominio):
    id_proceso_anonimizacion: uuid.UUID = None
    id_partner: uuid.UUID = None
    fecha_creacion: datetime = None
    datos: list[ov.Dato] = None