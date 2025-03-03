from pulsar.schema import *
from saludtech.servicio_estandarizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class ProcesoEstandarizacionCreadoPayload(Record):
    id_proceso_estandarizacion = String()
    id_proceso_ingestion = String()
    fecha_creacion = Long()


class EventoProcesoEstandarizacionCreado(EventoIntegracion):
    data = ProcesoEstandarizacionCreadoPayload()


class ProcesoEstandarizacionCompletadoPayload(Record):
    id_proceso_estandarizacion = String()
    id_proceso_ingestion = String()
    fecha_actualizacion = Long()


class EventoProcesoEstandarizacionCompletado(EventoIntegracion):
    data = ProcesoEstandarizacionCompletadoPayload()