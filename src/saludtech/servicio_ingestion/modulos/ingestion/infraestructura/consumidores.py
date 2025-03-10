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
def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-proceso_ingestion2', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='saludtech-sub-eventos',schema=AvroSchema(EventoProcesoIngestionCreado))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-proceso_ingestion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='saludtech-sub-comandos',schema=AvroSchema(ComandoCrearProcesoIngestion))

        while True:
            mensaje = consumidor.receive()
          
            print(f'Comando recibido: {mensaje.value().data}')
            mc= mensaje.value().data
            imagenes= ast.literal_eval(mc.imagenes)
            imagenes_comando:list[ImagenDTO] = list()
            for imagen in imagenes:
                imagen_dto: ImagenDTO = ImagenDTO(imagen.get('tipo'),imagen.get('archivo'))
                imagenes_comando.append(imagen_dto)

            comando= CrearProcesoIngestion(fecha_creacion=mc.fecha_creacion,fecha_actualizacion=mc.fecha_actualizacion,id=mc.id_proceso_ingestion,id_partner=mc.id_partner,imagenes=imagenes_comando)
            ejecutar_commando(comando)
            
            print("comando ejecutado")
            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()