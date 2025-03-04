from saludtech.servicio_estandarizacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from saludtech.servicio_estandarizacion.seedwork.aplicacion.queries import ejecutar_query as query
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.repositorios import RepositorioProcesoEstandarizacion
from dataclasses import dataclass
from .base import ProcesoEstandarizacionQueryBaseHandler
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.mapeadores import MapeadorProcesoEstandarizacion
import uuid

@dataclass
class ObtenerProcesoEstandarizacion(Query):
    id: str


class ObtenerProcesoEstandarizacionHandler(ProcesoEstandarizacionQueryBaseHandler):

    def handle(self, query: ObtenerProcesoEstandarizacion) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProcesoEstandarizacion.__class__)
        proceso_estandarizacion = self.fabrica_estandarizacion.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorProcesoEstandarizacion())
        return QueryResultado(resultado=proceso_estandarizacion)


@query.register(ObtenerProcesoEstandarizacion)
def ejecutar_query_obtener_proceso_estandarizacion(query: ObtenerProcesoEstandarizacion):
    handler = ObtenerProcesoEstandarizacionHandler()
    return handler.handle(query)