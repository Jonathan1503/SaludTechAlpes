from pydispatch import dispatcher

from .handlers import HandlerProcesoAnonimizacionIntegracion

from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionCreado

dispatcher.connect(HandlerProcesoAnonimizacionIntegracion.handle_proceso_anonimizacion_creado, signal=f'{ProcesoAnonimizacionCreado.__name__}Integracion')