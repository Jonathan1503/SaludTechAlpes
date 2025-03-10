from saludtech.servicio_ingestion.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from saludtech.servicio_ingestion.seedwork.aplicacion.comandos import Comando
from saludtech.servicio_ingestion.seedwork.dominio.eventos import EventoDominio

from aeroalpes.modulos.sagas.aplicacion.comandos.cliente import RegistrarUsuario, ValidarUsuario
from aeroalpes.modulos.sagas.aplicacion.comandos.pagos import PagarReserva, RevertirPago
from aeroalpes.modulos.sagas.aplicacion.comandos.gds import ConfirmarReserva, RevertirConfirmacion
from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.comandos.crear_proceso_ingestion import CrearProcesoIngestion
from saludtech.servicio_ingestion.modulos.ingestion.aplicacion.comandos.cancelar_proceso_ingestion import CancelarProcesoIngestion
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.comandos.anonimizar_proceso import AnonimizarProceso
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.comandos.cancelar_proceso_anonimizacion import CancelarProcesoAnonimizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.comandos.procesar_estandarizacion import ProcesarEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.comandos.cancelar_proceso_estandarizacion import CancelarProcesoEstandarizacion
from aeroalpes.modulos.vuelos.aplicacion.comandos.aprobar_reserva import AprobarReserva
from aeroalpes.modulos.vuelos.aplicacion.comandos.cancelar_reserva import CancelarReserva
from saludtech.servicio_ingestion.modulos.ingestion.dominio.eventos import ProcesoIngestionCreado, ReservaCancelada, ReservaAprobada, CreacionProcesoIngestionFallido, AprobacionReservaFallida
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionCreado,CreacionProcesoAnonimizacionFallido
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.eventos import ProcesoEstandarizacionCreado,CreacionProcesoEstandarizacionFallido
from aeroalpes.modulos.sagas.dominio.eventos.pagos import ReservaPagada, PagoRevertido
from aeroalpes.modulos.sagas.dominio.eventos.gds import ReservaGDSConfirmada, ConfirmacionGDSRevertida, ConfirmacionFallida


class CoordinadorReservas(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearProcesoIngestion, evento=ProcesoIngestionCreado, error=CreacionProcesoIngestionFallido, compensacion=CancelarProcesoIngestion),
            Transaccion(index=2, comando=AnonimizarProceso, evento=ProcesoAnonimizacionCreado, error=CreacionProcesoAnonimizacionFallido, compensacion=CancelarProcesoAnonimizacion),
            Transaccion(index=3, comando=ProcesarEstandarizacion, evento=ProcesoEstandarizacionCreado, error=CreacionProcesoEstandarizacionFallido, compensacion=CancelarProcesoEstandarizacion),
            Transaccion(index=4, comando=AprobarReserva, evento=ReservaAprobada, error=AprobacionReservaFallida, compensacion=CancelarReserva),
            Fin(index=5)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])
    
    def terminar():
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        # TODO Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        ...

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        # TODO Transforma un evento en la entrada de un comando
        # Por ejemplo si el evento que llega es ReservaCreada y el tipo_comando es PagarReserva
        # Debemos usar los atributos de ReservaCreada para crear el comando PagarReserva
        ...


# TODO Agregue un Listener/Handler para que se puedan redireccionar eventos de dominio
def oir_mensaje(mensaje):
    if isinstance(mensaje, EventoDominio):
        coordinador = CoordinadorReservas()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")