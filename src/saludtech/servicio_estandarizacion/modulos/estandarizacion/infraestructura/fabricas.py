from dataclasses import dataclass, field
from saludtech.servicio_estandarizacion.seedwork.dominio.fabricas import Fabrica
from saludtech.servicio_estandarizacion.seedwork.dominio.repositorios import Repositorio
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.repositorios import RepositorioProcesoEstandarizacion
from .repositorios import RepositorioProcesoEstandarizacionPg
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioProcesoEstandarizacion.__class__:
            return RepositorioProcesoEstandarizacionPg()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion()