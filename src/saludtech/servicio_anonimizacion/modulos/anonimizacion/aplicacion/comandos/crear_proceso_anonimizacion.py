from saludtech.servicio_anonimizacion.seedwork.aplicacion.comandos import Comando
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.dto import DatoDTO, ProcesoAnonimizacionDTO
from .base import CrearProcesoAnonimizacionBaseHandler
from dataclasses import dataclass, field
from saludtech.servicio_anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.entidades import ProcesoAnonimizacion
from saludtech.servicio_anonimizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorProcesoAnonimizacion
from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.repositorios import RepositorioProcesoAnonimizacion
import traceback
from saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.despachadores import Despachador

@dataclass
class CrearProcesoAnonimizacion(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    datos: list[DatoDTO]
    id_partner: str

class CrearProcesoAnonimizacionHandler(CrearProcesoAnonimizacionBaseHandler):
    
    def handle(self, comando: CrearProcesoAnonimizacion):
        
        proceso_anonimizacion_dto = ProcesoAnonimizacionDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   datos=comando.datos,
            id_partner=comando.id_partner)
        
        print(comando.datos)

        proceso_anonimizacion: ProcesoAnonimizacion = self.fabrica_anonimizacion.crear_objeto(proceso_anonimizacion_dto, MapeadorProcesoAnonimizacion())
        proceso_anonimizacion.crear_proceso_anonimizacion(proceso_anonimizacion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProcesoAnonimizacion.__class__)
        try:
            UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, proceso_anonimizacion)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()
        except Exception: 
            print(traceback.format_exc())
            UnidadTrabajoPuerto.rollback()

@comando.register(CrearProcesoAnonimizacion)
def ejecutar_comando_crear_proceso_anonimizacion(comando: CrearProcesoAnonimizacion):
    handler = CrearProcesoAnonimizacionHandler()
    handler.handle(comando)