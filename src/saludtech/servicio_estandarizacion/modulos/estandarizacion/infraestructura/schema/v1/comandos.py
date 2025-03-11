from pulsar.schema import *
from dataclasses import dataclass, field
from saludtech.servicio_estandarizacion.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


class Imagen(Record):
    tipo = String()
    archivo = String()
    archivo_estandarizado = Boolean()

class ComandoProcesarEstandarizacionPayload(Record):
    id_proceso_ingestion = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    id_proceso_estandarizacion = String()
    imagenes = String()
    estado = String()

class ComandoProcesarEstandarizacion(ComandoIntegracion):
    data = ComandoProcesarEstandarizacionPayload()