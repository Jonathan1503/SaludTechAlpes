import pulsar, _pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import ast
from datetime import datetime
from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoProcesoAnonimizacionCreado
from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearProcesoAnonimizacion
from saludtech.servicio_anonimizacion.seedwork.infraestructura import utils
from saludtech.servicio_anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.comandos.crear_proceso_anonimizacion import CrearProcesoAnonimizacion
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.dto import DatoDTO
from saludtech.servicio_anonimizacion.modulos.ingestion.infraestructura.schema.v1.eventos import EventoProcesoIngestionCreado

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        # Suscribirse a eventos de ingestion para procesarlos
        consumidor = cliente.subscribe('eventos-proceso_ingestion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-eventos', schema=AvroSchema(EventoProcesoIngestionCreado))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento de ingestion recibido: {mensaje.value().data}')
            
            # Procesar el evento de ingestion para crear un comando de anonimizacion
            mc = mensaje.value().data
            imagenes = ast.literal_eval(mc.imagenes)
            datos: list[DatoDTO] = list()
            
            # Convertir las imágenes a datos para anonimización
            for imagen in imagenes:
                dato_dto = DatoDTO(tipo="imagen", contenido=imagen.get('archivo'), anonimizado=False)
                datos.append(dato_dto)
            
            # Crear y ejecutar el comando de anonimización
            comando = CrearProcesoAnonimizacion(
                fecha_creacion=str(datetime.now()),
                fecha_actualizacion=str(datetime.now()),
                id=str(uuid.uuid4()),
                id_partner=mc.id_partner,
                datos=datos
            )
            
            ejecutar_commando(comando)
            print("Proceso de anonimización iniciado")
            
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
        consumidor = cliente.subscribe('comandos-proceso_anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-comandos', schema=AvroSchema(ComandoCrearProcesoAnonimizacion))

        while True:
            mensaje = consumidor.receive()
          
            print(f'Comando recibido: {mensaje.value().data}')
            mc = mensaje.value().data
            datos = ast.literal_eval(mc.datos)
            datos_comando: list[DatoDTO] = list()
            
            for dato in datos:
                dato_dto = DatoDTO(dato.get('tipo'), dato.get('contenido'), dato.get('anonimizado', False))
                datos_comando.append(dato_dto)

            comando = CrearProcesoAnonimizacion(fecha_creacion=mc.fecha_creacion, fecha_actualizacion=mc.fecha_actualizacion, id=mc.id_proceso_anonimizacion, id_partner=mc.id_partner, datos=datos_comando)
            ejecutar_commando(comando)
            
            print("Comando ejecutado")
            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()