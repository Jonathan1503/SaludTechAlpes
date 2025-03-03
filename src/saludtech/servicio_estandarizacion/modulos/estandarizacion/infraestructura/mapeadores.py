from saludtech.servicio_estandarizacion.seedwork.dominio.repositorios import Mapeador
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.objetos_valor import ImagenEstandarizada, EstadoEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.entidades import ProcesoEstandarizacion, Region
from .dto import ProcesoEstandarizacion as ProcesoEstandarizacionDTO
from .dto import ImagenEstandarizada as ImagenEstandarizadaDTO

class MapeadorProcesoEstandarizacion(Mapeador):
   
    def obtener_tipo(self) -> type:
        return ProcesoEstandarizacion.__class__

    def entidad_a_dto(self, entidad: ProcesoEstandarizacion) -> ProcesoEstandarizacionDTO:
        
        proceso_estandarizacion_dto = ProcesoEstandarizacionDTO()
        proceso_estandarizacion_dto.fecha_creacion = entidad.fecha_creacion
        proceso_estandarizacion_dto.fecha_actualizacion = entidad.fecha_actualizacion
        proceso_estandarizacion_dto.id = str(entidad.id)
        proceso_estandarizacion_dto.id_proceso_ingestion = str(entidad.id_proceso_ingestion)
        proceso_estandarizacion_dto.estado = entidad.estado.estado

        imagenes_dto = list()
        
        for imagen in entidad.imagenes:
            imagen_dto = ImagenEstandarizadaDTO()
            imagen_dto.tipo = imagen.tipo
            imagen_dto.archivo = imagen.archivo
            imagen_dto.archivo_estandarizado = imagen.archivo_estandarizado
            imagenes_dto.append(imagen_dto)

        proceso_estandarizacion_dto.imagenes = imagenes_dto

        return proceso_estandarizacion_dto

    def dto_a_entidad(self, dto: ProcesoEstandarizacionDTO) -> ProcesoEstandarizacion:
        proceso_estandarizacion = ProcesoEstandarizacion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        proceso_estandarizacion.id_proceso_ingestion = dto.id_proceso_ingestion
        proceso_estandarizacion.estado = EstadoEstandarizacion(estado=dto.estado)
        proceso_estandarizacion.imagenes = list()

        for imagen_dto in dto.imagenes:
            imagen=ImagenEstandarizada(
                tipo=imagen_dto.tipo,
                archivo=imagen_dto.archivo,
                archivo_estandarizado=imagen_dto.archivo_estandarizado
            )
            proceso_estandarizacion.imagenes.append(imagen)
        
        return proceso_estandarizacion
