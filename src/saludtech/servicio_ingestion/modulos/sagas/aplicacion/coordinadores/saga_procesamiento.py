from saludtech.servicio_ingestion.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from saludtech.servicio_ingestion.seedwork.aplicacion.comandos import Comando
from saludtech.servicio_ingestion.seedwork.dominio.eventos import EventoDominio

from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.comandos.crear_proceso_ingestion import CrearProcesoIngestion
from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.comandos.cancelar_proceso_ingestion import CancelarProcesoIngestion
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.comandos.anonimizacion import AnonimizarProceso,CancelarProcesoAnonimizacion
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.comandos.estandarizacion import ProcesarEstandarizacion, CancelarProcesoEstandarizacion
from saludtech.servicio_ingestion.modulos.ingestion.dominio.eventos import ProcesoIngestionCreado, CreacionProcesoIngestionFallido
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionCreado,CreacionProcesoAnonimizacionFallido
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.eventos import ProcesoEstandarizacionCreado,CreacionProcesoEstandarizacionFallido
from saludtech.servicio_ingestion.modulos.sagas.infraestructura.dto import EventoDataLog
from saludtech.servicio_ingestion.config.db import db
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.mapeadores import MapeadorSagas
#from saludtech.servicio_ingestion.api  import __init__
class CoordinadorProcesos(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearProcesoIngestion, evento=ProcesoIngestionCreado, error=CreacionProcesoIngestionFallido, compensacion=CancelarProcesoIngestion),
            Transaccion(index=2, comando=AnonimizarProceso, evento=ProcesoAnonimizacionCreado, error=CreacionProcesoAnonimizacionFallido, compensacion=CancelarProcesoAnonimizacion),
            Transaccion(index=3, comando=ProcesarEstandarizacion, evento=ProcesoEstandarizacionCreado, error=CreacionProcesoEstandarizacionFallido, compensacion=CancelarProcesoEstandarizacion),
            Fin(index=5)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])
    
    def terminar():
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        id_correlacion = mensaje.id_correlacion
        evento = str(mensaje)
        evento_datalog = EventoDataLog()
        evento_datalog.id=id_correlacion
        evento_datalog.evento = evento
        db.session.add(evento_datalog)

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
       
        mapeador = MapeadorSagas()
      
        if tipo_comando == AnonimizarProceso:
            comando = mapeador.evento_a_anonimizacion(evento)
            return comando
        elif tipo_comando == ProcesarEstandarizacion:
            comando = mapeador.evento_a_estandarizacion(evento)
            return comando
             



def oir_mensaje(mensaje):
    print(type(mensaje))
    print("bb")

    if isinstance(mensaje, EventoDominio):
        coordinador=CoordinadorProcesos()
        coordinador.inicializar_pasos()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")