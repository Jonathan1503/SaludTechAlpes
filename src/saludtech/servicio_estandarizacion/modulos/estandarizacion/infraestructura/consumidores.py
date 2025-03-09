import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.schema.v1.eventos import EventoProcesoEstandarizacionCreado, EventoProcesoEstandarizacionCompletado
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.schema.v1.comandos import ComandoProcesarEstandarizacion
from saludtech.servicio_estandarizacion.seedwork.infraestructura import utils
from saludtech.servicio_estandarizacion.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.comandos.procesar_estandarizacion import ProcesarEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.dto import ImagenEstandarizadaDTO


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-proceso_ingestion', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='estandarizacion-sub-eventos',
                                       schema=AvroSchema(EventoProcesoEstandarizacionCreado))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            # Aquí procesaríamos el evento y crearíamos un comando para estandarizacion
            # Por ejemplo, al recibir un evento de anonimizacion completado, iniciaríamos el proceso de estandarizacion

            consumidor.acknowledge(mensaje)

        cliente.close()
    except Exception as e:
        logging.error(f'ERROR: Suscribiendose al tópico de eventos: {str(e)}')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-proceso_anonimizacion', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='anonimizacion-sub-comandos',
                                       schema=AvroSchema(ComandoProcesarEstandarizacion))

        while True:
            mensaje = consumidor.receive()

            print(f'Comando recibido: {mensaje.value().data}')
            mc = mensaje.value().data

            imagenes = []
            for img in mc.imagenes:
                imagen_dto = ImagenEstandarizadaDTO(
                    tipo=img.tipo,
                    archivo=img.archivo,
                    archivo_estandarizado=img.archivo_estandarizado
                )
                imagenes.append(imagen_dto)

            comando = ProcesarEstandarizacion(
                fecha_creacion=mc.fecha_creacion,
                fecha_actualizacion=mc.fecha_actualizacion,
                id=mc.id_proceso_estandarizacion,
                id_proceso_ingestion=mc.id_proceso_ingestion,
                imagenes=imagenes,
                estado=mc.estado
            )
            ejecutar_commando(comando)

            print("comando ejecutado")
            consumidor.acknowledge(mensaje)

        cliente.close()
    except Exception as e:
        logging.error(f'ERROR: Suscribiendose al tópico de comandos: {str(e)}')
        traceback.print_exc()
        if cliente:
            cliente.close()
