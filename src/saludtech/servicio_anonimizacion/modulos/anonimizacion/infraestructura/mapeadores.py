from saludtech.servicio_anonimizacion.seedwork.dominio.repositorios import Mapeador
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.objetos_valor import Dato
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.entidades import ProcesoAnonimizacion
from .dto import ProcesoAnonimizacion as ProcesoAnonimizacionDTO
from .dto import Dato as DatoDTO

class MapeadorProcesoAnonimizacion(Mapeador):
   
    def obtener_tipo(self) -> type:
        return ProcesoAnonimizacion.__class__

    def entidad_a_dto(self, entidad: ProcesoAnonimizacion) -> ProcesoAnonimizacionDTO:
        
        proceso_anonimizacion_dto = ProcesoAnonimizacionDTO()
        proceso_anonimizacion_dto.fecha_creacion = entidad.fecha_creacion
        proceso_anonimizacion_dto.fecha_actualizacion = entidad.fecha_actualizacion
        proceso_anonimizacion_dto.id = str(entidad.id)
        proceso_anonimizacion_dto.id_partner = str(entidad.id_partner)

        datos_dto = list()
        
        for dato in entidad.datos:
            dato_dto = DatoDTO()
            dato_dto.tipo = dato.tipo
            dato_dto.contenido = dato.contenido
            dato_dto.anonimizado = dato.anonimizado
            datos_dto.append(dato_dto)

        proceso_anonimizacion_dto.datos = datos_dto

        return proceso_anonimizacion_dto

    def dto_a_entidad(self, dto: ProcesoAnonimizacionDTO) -> ProcesoAnonimizacion:
        proceso_anonimizacion = ProcesoAnonimizacion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        proceso_anonimizacion.id_partner = dto.id_partner
        proceso_anonimizacion.datos = list()

        datos_dto: list[DatoDTO] = dto.datos
        for dato_dto in datos_dto:
            dato = Dato(tipo=dato_dto.tipo, contenido=dato_dto.contenido, anonimizado=dato_dto.anonimizado)
            proceso_anonimizacion.datos.extend(dato)
        
        return proceso_anonimizacion