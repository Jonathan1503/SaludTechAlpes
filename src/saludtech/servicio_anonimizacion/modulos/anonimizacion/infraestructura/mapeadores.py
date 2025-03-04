from saludtech.servicio_anonimizacion.seedwork.dominio.repositorios import Mapeador
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.objetos_valor import ImagenAnonimizada
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.entidades import ProcesoAnonimizacion
from .dto import ProcesoAnonimizacion as ProcesoAnonimizacionDTO
from .dto import ImagenAnonimizada as ImagenAnonimizadaDTO

class MapeadorProcesoAnonimizacion(Mapeador):
    def obtener_tipo(self) -> type:
        return ProcesoAnonimizacion.__class__

    def entidad_a_dto(self, entidad: ProcesoAnonimizacion) -> ProcesoAnonimizacionDTO:
        proceso_anonimizacion_dto = ProcesoAnonimizacionDTO()
        proceso_anonimizacion_dto.fecha_creacion = entidad.fecha_creacion
        proceso_anonimizacion_dto.fecha_actualizacion = entidad.fecha_actualizacion
        proceso_anonimizacion_dto.id = str(entidad.id)
        proceso_anonimizacion_dto.id_proceso_original = str(entidad.id_proceso_original)

        imagenes_dto = []
        
        for imagen in entidad.imagenes:
            imagen_dto = ImagenAnonimizadaDTO()
            imagen_dto.tipo = imagen.tipo
            imagen_dto.archivo = imagen.archivo
            imagen_dto.archivo_original = imagen.archivo_original
            imagenes_dto.append(imagen_dto)

        proceso_anonimizacion_dto.imagenes = imagenes_dto
        return proceso_anonimizacion_dto

    def dto_a_entidad(self, dto: ProcesoAnonimizacionDTO) -> ProcesoAnonimizacion:
        proceso_anonimizacion = ProcesoAnonimizacion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        proceso_anonimizacion.id_proceso_original = dto.id_proceso_original
        proceso_anonimizacion.imagenes = []

        if hasattr(dto, 'imagenes'):
            for imagen_dto in dto.imagenes:
                imagen = ImagenAnonimizada(
                    tipo=imagen_dto.tipo,
                    archivo=imagen_dto.archivo,
                    archivo_original=imagen_dto.archivo_original
                )
                proceso_anonimizacion.imagenes.append(imagen)
        
        return proceso_anonimizacion