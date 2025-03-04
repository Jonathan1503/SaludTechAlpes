from __future__ import annotations
from dataclasses import dataclass, field

import saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.objetos_valor as ov
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.eventos import ProcesoEstandarizacionCreado, ProcesoEstandarizacionCompletado
from saludtech.servicio_estandarizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class ProcesoEstandarizacion(AgregacionRaiz):
    id_proceso_ingestion: uuid.UUID = field(hash=True, default=None)
    imagenes: list[ov.ImagenEstandarizada] = field(default_factory=list[ov.ImagenEstandarizada])
    estado: ov.EstadoEstandarizacion = field(default_factory=ov.EstadoEstandarizacion)

    def crear_proceso_estandarizacion(self, proceso_estandarizacion: ProcesoEstandarizacion):
        self.id_proceso_ingestion = proceso_estandarizacion.id_proceso_ingestion
        self.imagenes = proceso_estandarizacion.imagenes
        self.estado = ov.EstadoEstandarizacion(estado="PENDIENTE")

        self.agregar_evento(ProcesoEstandarizacionCreado(
            id_proceso_estandarizacion=self.id,
            id_proceso_ingestion=self.id_proceso_ingestion,
            fecha_creacion=self.fecha_creacion
        ))

    def completar_estandarizacion(self):
        self.estado = ov.EstadoEstandarizacion(estado="COMPLETADO")

        self.agregar_evento(ProcesoEstandarizacionCompletado(
            id_proceso_estandarizacion=self.id,
            id_proceso_ingestion=self.id_proceso_ingestion,
            fecha_actualizacion=self.fecha_actualizacion
        ))
