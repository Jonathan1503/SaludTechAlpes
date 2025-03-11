import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import ast
from saludtech.servicio_ingestion.modulos.ingestion.infraestructura.schema.v1.eventos import EventoProcesoIngestionCreado
from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoProcesoAnonimizacionCreado
#from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.schema.v1.eventos import EventoProcesoAnonimizacionCreado
from saludtech.servicio_ingestion.modulos.ingestion.infraestructura.schema.v1.comandos import ComandoCrearProcesoIngestion
from saludtech.servicio_ingestion.seedwork.infraestructura import utils
from saludtech.servicio_ingestion.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.comandos.crear_proceso_ingestion import CrearProcesoIngestion
from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.dto import ImagenDTO
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.coordinadores.saga_procesamiento import oir_mensaje
import saludtech.servicio_ingestion.modulos.ingestion.dominio.objetos_valor as ov
from saludtech.servicio_ingestion.modulos.ingestion.dominio.eventos import ProcesoIngestionCreado
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionCreado
from datetime import datetime
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.objetos_valor import ImagenAnonimizada
def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-proceso_ingestion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='saludtech-sub-eventos',schema=AvroSchema(EventoProcesoIngestionCreado))
        while True:
            mensaje = consumidor.receive()
            mc=mensaje.value().data
            imagenes = ast.literal_eval(mc.imagenes)
            imagenes_evento:list[ov.Imagen] = list()
            for imagen in imagenes:
                imagen_dto: ov.Imagen = ov.Imagen(tipo=imagen.get('tipo'),archivo=imagen.get('archivo'))
                imagenes_evento.append(imagen_dto)
            evento_dominio = ProcesoIngestionCreado(
                id_proceso_ingestion = uuid.UUID(mc.id_proceso_ingestion),
                id_partner = uuid.uuid4(),
                fecha_creacion = datetime.fromtimestamp(mc.fecha_creacion / 1000.0).strftime('%Y-%m-%d'),
                imagenes= imagenes_evento
                
            )
            print(f'Evento recibido2: {mensaje.value().data}')
            oir_mensaje(evento_dominio)
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
def suscribirse_a_eventos2():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-proceso_anonimizacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='estandarizacion-sub-eventos',schema=AvroSchema(EventoProcesoAnonimizacionCreado))
        while True:
            mensaje = consumidor.receive()
            mc=mensaje.value().data
            print("hollaa")
            imagenes = ast.literal_eval(mc.imagenes_anonimizadas)
            imagenes_evento:list[ImagenAnonimizada] = list()
            for imagen in imagenes:
                imagen_dto: ImagenAnonimizada = ImagenAnonimizada(tipo=imagen.get('tipo'),archivo=imagen.get('archivo'),archivo_original=imagen.get('archivo'))
                imagenes_evento.append(imagen_dto)
            evento_dominio = ProcesoAnonimizacionCreado(
                id_proceso_anonimizacion = uuid.UUID(mc.id_proceso_anonimizacion),
                id_proceso_original = uuid.UUID(mc.id_proceso_original),
                fecha_creacion = datetime.fromtimestamp(mc.fecha_creacion / 1000.0).strftime('%Y-%m-%d'),
                imagenes= imagenes_evento
                
            )
            print(f'Evento recibido2: {mensaje.value().data}')
            oir_mensaje(evento_dominio)
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

