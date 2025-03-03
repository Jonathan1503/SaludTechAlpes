from saludtech.servicio_estandarizacion.config.db import db
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.repositorios import RepositorioProcesoEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.entidades import ProcesoEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.fabricas import FabricaEstandarizacion
from .dto import ProcesoEstandarizacion as ProcesoEstandarizacionDto
from .mapeadores import MapeadorProcesoEstandarizacion
from uuid import UUID


class RepositorioProcesoEstandarizacionPg(RepositorioProcesoEstandarizacion):

    def __init__(self):
        self._fabrica_estandarizacion: FabricaEstandarizacion = FabricaEstandarizacion()

    @property
    def fabrica_estandarizacion(self):
        return self._fabrica_estandarizacion

    def obtener_por_id(self, id: UUID) -> ProcesoEstandarizacion:
        proceso_estandarizacion_dto = db.session.query(ProcesoEstandarizacionDto).filter_by(id=str(id)).one()
        return self._fabrica_estandarizacion.crear_objeto(proceso_estandarizacion_dto, MapeadorProcesoEstandarizacion())

    def obtener_todos(self) -> list[ProcesoEstandarizacion]:
        # TODO
        raise NotImplementedError

    def agregar(self, proceso_estandarizacion: ProcesoEstandarizacion):
        proceso_estandarizacion_dto = self._fabrica_estandarizacion.crear_objeto(proceso_estandarizacion, MapeadorProcesoEstandarizacion())
        db.session.add(proceso_estandarizacion_dto)

    def actualizar(self, proceso_estandarizacion: ProcesoEstandarizacion):
        proceso_estandarizacion_dto = db.session.query(ProcesoEstandarizacionDto).filter_by(id=str(proceso_estandarizacion.id)).one()

        proceso_estandarizacion_dto.fecha_actualizacion = proceso_estandarizacion.fecha_actualizacion
        proceso_estandarizacion_dto.estado = proceso_estandarizacion.estado.estado

        db.session.commit()

    def eliminar(self, proceso_estandarizacion_id: UUID):
        # TODO
        raise NotImplementedError