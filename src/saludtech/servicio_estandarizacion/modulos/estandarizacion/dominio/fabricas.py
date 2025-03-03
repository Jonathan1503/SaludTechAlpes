from .excepciones import TipoObjetoNoExisteEnDominioEstandarizacionExcepcion
from .entidades import ProcesoEstandarizacion
from saludtech.servicio_estandarizacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from saludtech.servicio_estandarizacion.seedwork.dominio.fabricas import Fabrica
from saludtech.servicio_estandarizacion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaProcesoEstandarizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            proceso_estandarizacion: ProcesoEstandarizacion = mapeador.dto_a_entidad(obj)

            return proceso_estandarizacion

@dataclass
class FabricaEstandarizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == ProcesoEstandarizacion.__class__:
            fabrica_estandarizacion = _FabricaProcesoEstandarizacion()
            return fabrica_estandarizacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioEstandarizacionExcepcion()