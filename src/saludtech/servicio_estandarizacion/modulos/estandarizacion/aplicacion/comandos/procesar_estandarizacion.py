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

        proceso_estandarizacion_dto = ProcesoEstandarizacionDTO(
            fecha_actualizacion=comando.fecha_actualizacion
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
            UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, proceso_estandarizacion)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

            # Aquí simulamos el proceso de estandarizacion
            # En un sistema real, este código iría en un worker separado
            for i, imagen in enumerate(proceso_estandarizacion.imagenes):
                # Simular el proceso de estandarizacion
                proceso_estandarizacion.imagenes[i] = ImagenEstandarizada(
                    tipo=imagen.tipo,
                    archivo=imagen.archivo,
                    archivo_estandarizado=f"estandarizado_{imagen.archivo}"
                )

            proceso_estandarizacion.completar_estandarizacion()

            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, proceso_estandarizacion)
            UnidadTrabajoPuerto.commit()

        except Exception:
            print(traceback.format_exc())
            UnidadTrabajoPuerto.rollback()


@comando.register(ProcesarEstandarizacion)
def ejecutar_comando_procesar_estandarizacion(comando: ProcesarEstandarizacion):
    handler = ProcesarEstandarizacionHandler()
    handler.handle(comando)