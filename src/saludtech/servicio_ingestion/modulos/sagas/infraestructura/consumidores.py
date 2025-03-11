import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import ast
from saludtech.servicio_ingestion.modulos.ingestion.infraestructura.schema.v1.eventos import EventoProcesoIngestionCreado
from saludtech.servicio_ingestion.modulos.ingestion.infraestructura.schema.v1.comandos import ComandoCrearProcesoIngestion
from saludtech.servicio_ingestion.seedwork.infraestructura import utils
from saludtech.servicio_ingestion.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.comandos.crear_proceso_ingestion import CrearProcesoIngestion
from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.dto import ImagenDTO
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.coordinadores.saga_procesamiento import oir_mensaje
def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-proceso_ingestion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='saludtech-sub-eventos',schema=AvroSchema(EventoProcesoIngestionCreado))
        consumidor = cliente.subscribe('eventos-proceso_anonimizacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='estandarizacion-sub-eventos',schema=AvroSchema(EventoProcesoAnonimizacionCreado))
        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')
            oir_mensaje(mensaje)
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

