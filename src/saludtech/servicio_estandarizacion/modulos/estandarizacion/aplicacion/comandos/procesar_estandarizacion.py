from saludtech.servicio_estandarizacion.seedwork.aplicacion.comandos import Comando
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.dto import ImagenEstandarizadaDTO, ProcesoEstandarizacionDTO
from .base import ProcesarEstandarizacionBaseHandler
from dataclasses import dataclass, field
from saludtech.servicio_estandarizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.entidades import ProcesoEstandarizacion
from saludtech.servicio_estandarizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.mapeadores import MapeadorProcesoEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.repositorios import RepositorioProcesoEstandarizacion
import traceback
from pydispatch import dispatcher


@dataclass
class ProcesarEstandarizacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    imagenes: list[ImagenEstandarizadaDTO]
    id_proceso_ingestion: str
    estado: str


class ProcesarEstandarizacionHandler(ProcesarEstandarizacionBaseHandler):

    def handle(self, comando: ProcesarEstandarizacion):
        from saludtech.servicio_estandarizacion.config.db import db
        proceso_estandarizacion_dto = ProcesoEstandarizacionDTO(
            fecha_actualizacion=comando.fecha_creacion
            , fecha_creacion=comando.fecha_creacion
            , id=comando.id
            , imagenes=comando.imagenes
            , id_proceso_ingestion=comando.id_proceso_ingestion
            , estado=comando.estado)

        proceso_estandarizacion: ProcesoEstandarizacion = self.fabrica_estandarizacion.crear_objeto(proceso_estandarizacion_dto,
                                                                                              MapeadorProcesoEstandarizacion())
        proceso_estandarizacion.crear_proceso_estandarizacion(proceso_estandarizacion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProcesoEstandarizacion.__class__)
        try:
            repositorio.agregar(proceso_estandarizacion)
            db.session.commit()
            eventos=proceso_estandarizacion.eventos
            for evento in eventos:
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
                dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

        except Exception:
            print(traceback.format_exc())
            db.session.rollback()

      


@comando.register(ProcesarEstandarizacion)
def ejecutar_comando_procesar_estandarizacion(comando: ProcesarEstandarizacion):
    handler = ProcesarEstandarizacionHandler()
    handler.handle(comando)