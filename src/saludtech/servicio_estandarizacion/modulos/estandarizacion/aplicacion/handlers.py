from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.eventos import ProcesoEstandarizacionCreado, ProcesoEstandarizacionCompletado
from saludtech.servicio_estandarizacion.seedwork.aplicacion.handlers import Handler
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.despachadores import Despachador

class HandlerProcesoEstandarizacionIntegracion(Handler):

    @staticmethod
    def handle_proceso_estandarizacion_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-proceso_estandarizacion')

    @staticmethod
    def handle_proceso_estandarizacion_completado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-proceso_estandarizacion_completado')