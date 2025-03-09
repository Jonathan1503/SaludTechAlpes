import pulsar
from pulsar.schema import *

from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoProcesoAnonimizacionCreado, ProcesoAnonimizacionCreadoPayload
from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearProcesoAnonimizacion, ComandoCrearProcesoAnonimizacionPayload
from saludtech.servicio_anonimizacion.seedwork.infraestructura import utils

from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

        if topico == "comandos-proceso_anonimizacion":
            publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoCrearProcesoAnonimizacion))
        else:
            publicador = cliente.create_producer(topico, schema=AvroSchema(EventoProcesoAnonimizacionCreado))
        publicador.send(mensaje)
        print("comando_publicado")
        cliente.close()

    def publicar_evento(self, evento, topico):
        datos = list()

        for dato in evento.datos:
            datos.append({"tipo": dato.tipo, "contenido": dato.contenido, "anonimizado": dato.anonimizado})
            
        payload = ProcesoAnonimizacionCreadoPayload(
            id_proceso_anonimizacion=str(evento.id_proceso_anonimizacion), 
            id_partner=str(evento.id_partner), 
            fecha_creacion=int(datetime.strptime(evento.fecha_creacion, '%Y-%m-%d').timestamp() * 1000),
            datos=str(datos)
        )
        print("evento_publicado")
        evento_integracion = EventoProcesoAnonimizacionCreado(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoProcesoAnonimizacionCreado))

    def publicar_comando(self, comando, topico):
        datos = list()
        for dato in comando.datos:
            datos.append({"tipo": dato.tipo, "contenido": dato.contenido, "anonimizado": dato.anonimizado})
        
        print("Test")
        print(datos)
        print("Test")
        
        payload = ComandoCrearProcesoAnonimizacionPayload(
            id_partner=str(comando.id_partner),
            fecha_creacion=str(comando.fecha_creacion),
            fecha_actualizacion=str(comando.fecha_actualizacion),
            id_proceso_anonimizacion=str(comando.id),
            datos=str(datos)
        )
        
        print(payload.datos)
        comando_integracion = ComandoCrearProcesoAnonimizacion(data=payload)
        
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearProcesoAnonimizacion))