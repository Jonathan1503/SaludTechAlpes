import pulsar
from pulsar.schema import *

from saludtech.servicio_ingestion.modulos.ingestion.infraestructura.schema.v1.eventos import EventoProcesoIngestionCreado, ProcesoIngestionCreadoPayload
from saludtech.servicio_ingestion.modulos.ingestion.infraestructura.schema.v1.comandos import ComandoCrearProcesoIngestion, ComandoCrearProcesoIngestionPayload
from saludtech.servicio_ingestion.seedwork.infraestructura import utils
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.comandos.anonimizacion import AnonimizarProceso
from datetime import datetime
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.schema.v1.comandos import ComandoProcesarEstandarizacion,ComandoProcesarEstandarizacionPayload
from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoAnonimizarProcesoPayload,ComandoAnonimizarProceso
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.comandos.estandarizacion import ProcesarEstandarizacion

class Despachador:
    def _publicar_mensaje(self, mensaje, topico,schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        print("comando_publicado")
        cliente.close()


    def publicar_comando(self, comando):
        print("aaaaaa")
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        """imagenes= list()
        for imagen in comando.imagenes:
                imagenes.append({"tipo": imagen.tipo, "archivo": imagen.archivo})
        print("cccccc")
        print(imagenes)
        print("cccc")
        payload = ComandoCrearProcesoIngestionPayload(
            id_partner=str(comando.id_partner),
            fecha_creacion= str(comando.fecha_creacion),
            fecha_actualizacion= str(comando.fecha_actualizacion),
            id_proceso_ingestion= str(comando.id),
            imagenes= str(imagenes)
            
        )
        print(payload.imagenes)
        comando_integracion = ComandoCrearProcesoIngestion(data=payload)
        """
        print(comando)
        if isinstance(comando,AnonimizarProceso):
            imagenes = list()
            for imagen in comando.imagenes:
                imagenes.append({"tipo": imagen.tipo, "archivo": imagen.archivo,"archivo_original":imagen.archivo_original})
            payload = ComandoAnonimizarProcesoPayload(
                id_proceso_original = str(comando.id_proceso_original),
                fecha_creacion = str(comando.fecha_creacion),
                fecha_actualizacion = str(comando.fecha_actualizacion),
                imagenes= str(imagenes),
                id = str(comando.id),
            )
            evento_integracion = ComandoAnonimizarProceso(data=payload)
            self._publicar_mensaje(comando, "comandos-proceso_anonimizacion",AvroSchema(ComandoAnonimizarProceso))
            print("pasoaca")

        elif isinstance(comando,ProcesarEstandarizacion):
            imagenes = list()
            for imagen in comando.imagenes:
                imagenes.append({"tipo": imagen.tipo, "archivo": imagen.archivo,"archivo_estandarizado":imagen.archivo_estandarizado})
            payload = ComandoProcesarEstandarizacionPayload(
                id_proceso_ingestion = str(comando.id_proceso_ingestion),
                fecha_creacion = int(datetime.strptime(comando.fecha_creacion, '%Y-%m-%d').timestamp() * 1000),
                imagenes= str(imagenes),
                id_proceso_estandarizacion = str(comando.id),
                estado = str(comando.estado)
            )
            evento_integracion = ComandoProcesarEstandarizacion(data=payload)
            print("paso")
            self._publicar_mensaje(evento_integracion, "comandos-proceso_estandarizacion",AvroSchema(ComandoProcesarEstandarizacion))
        

