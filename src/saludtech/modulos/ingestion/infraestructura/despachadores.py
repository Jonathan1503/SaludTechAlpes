import pulsar
from pulsar.schema import *

from saludtech.modulos.ingestion.infraestructura.schema.v1.eventos import EventoProcesoIngestionCreado, ProcesoIngestionCreadoPayload
from saludtech.modulos.ingestion.infraestructura.schema.v1.comandos import ComandoCrearProcesoIngestion, ComandoCrearProcesoIngestionPayload
from saludtech.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico,schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        print(mensaje)
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoCrearProcesoIngestion))
        publicador.send(mensaje)
        print("comando_publicado")
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ProcesoIngestionCreadoPayload(
            id_proceso_ingestion=str(evento.id_proceso_ingestion), 
            id_partner=str(evento.id_partner), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        print("evento_publicado")
        evento_integracion = EventoProcesoIngestionCreado(data=payload)
        self._publicar_mensaje(evento_integracion, topico,AvroSchema(EventoProcesoIngestionCreado))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        imagenes= list()
        for imagen in comando.imagenes:
                imagenes.extend({"tipo": imagen.tipo, "archivo": imagen.archivo})
        payload = ComandoCrearProcesoIngestionPayload(
            id_partner=str(comando.id_partner),
            fecha_creacion= str(comando.fecha_creacion),
            fecha_actualizacion= str(comando.fecha_actualizacion),
            id_proceso_ingestion= str(comando.id),
            imagenes= imagenes
            
        )
        print(payload)
        comando_integracion = ComandoCrearProcesoIngestion(data=payload)
        print(comando_integracion)
        print("aaa")
        self._publicar_mensaje(comando_integracion, topico,AvroSchema(ComandoCrearProcesoIngestion))
