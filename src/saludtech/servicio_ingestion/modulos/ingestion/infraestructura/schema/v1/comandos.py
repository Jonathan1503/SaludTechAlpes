from pulsar.schema import *
from dataclasses import dataclass, field
from saludtech.servicio_ingestion.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearProcesoIngestionPayload(Record):
    id_partner=String()
    fecha_creacion= String()
    fecha_actualizacion= String()
    id_proceso_ingestion= String()
    imagenes= String()
    

class ComandoCrearProcesoIngestion(ComandoIntegracion):
    data = ComandoCrearProcesoIngestionPayload()