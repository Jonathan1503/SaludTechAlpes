from saludtech.servicio_estandarizacion.seedwork.aplicacion.queries import QueryHandler
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.fabricas import FabricaRepositorio
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.fabricas import FabricaEstandarizacion


class ProcesoEstandarizacionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_estandarizacion: FabricaEstandarizacion = FabricaEstandarizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_estandarizacion(self):
        return self._fabrica_estandarizacion