from pulsar.schema import *
from dataclasses import dataclass, field
from saludtech.servicio_anonimizacion.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearProcesoAnonimizacionPayload(Record):
    id_partner = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    id_proceso_anonimizacion = String()
    datos = String()

class ComandoCrearProcesoAnonimizacion(ComandoIntegracion):
    data = ComandoCrearProcesoAnonimizacionPayload()