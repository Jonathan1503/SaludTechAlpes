import pulsar
from pulsar.schema import *

from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.schema.v1.eventos import EventoProcesoEstandarizacionCreado, ProcesoEstandarizacionCreadoPayload, EventoProcesoEstandarizacionCompletado, ProcesoEstandarizacionCompletadoPayload
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.schema.v1.comandos import ComandoProcesarEstandarizacion, ComandoProcesarEstandarizacionPayload
from saludtech.servicio_estandarizacion.seedwork.infraestructura import utils

from datetime import datetime

epoch = datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        if topico == "eventos-proceso_estandarizacion":
            payload = ProcesoEstandarizacionCreadoPayload(
                id_proceso_estandarizacion=str(evento.id_proceso_estandarizacion),
                id_proceso_ingestion=str(evento.id_proceso_ingestion),
                fecha_creacion=int(datetime.strptime(evento.fecha_creacion, '%Y-%m-%d').timestamp() * 1000)
            )
            evento_integracion = EventoProcesoEstandarizacionCreado(data=payload)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoProcesoEstandarizacionCreado))

        elif topico == "eventos-proceso_estandarizacion_completado":
            payload = ProcesoEstandarizacionCompletadoPayload(
                id_proceso_estandarizacion=str(evento.id_proceso_estandarizacion),
                id_proceso_ingestion=str(evento.id_proceso_ingestion),
                fecha_actualizacion=int(datetime.strptime(evento.fecha_actualizacion, '%Y-%m-%d').timestamp() * 1000)
            )
            evento_integracion = EventoProcesoEstandarizacionCompletado(data=payload)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoProcesoEstandarizacionCompletado))

    def publicar_comando(self, comando, topico):
        imagenes= []
        for imagen in comando.imagenes:
                imagenes.append({"tipo": str(imagen.tipo), "archivo": str(imagen.archivo), "archivo_estandarizado": bool(imagen.archivo_estandarizado)})

        payload = ComandoProcesarEstandarizacionPayload(
            id_proceso_ingestion=str(comando.id_proceso_ingestion),
            fecha_creacion= str(comando.fecha_creacion),
            fecha_actualizacion= str(comando.fecha_actualizacion),
            id_proceso_estandarizacion= str(comando.id),
            imagenes= imagenes,
            estado=comando.estado
        )
       
        comando_integracion = ComandoProcesarEstandarizacion(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoProcesarEstandarizacion))
