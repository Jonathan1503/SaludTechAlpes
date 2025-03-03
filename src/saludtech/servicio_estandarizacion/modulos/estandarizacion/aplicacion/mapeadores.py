from saludtech.servicio_estandarizacion.seedwork.aplicacion.dto import Mapeador as AppMap
from saludtech.servicio_estandarizacion.seedwork.dominio.repositorios import Mapeador as RepMap
from .dto import ProcesoEstandarizacionDTO, ImagenEstandarizadaDTO
from saludtech.servicio_estandarizacion.seedwork.dominio.repositorios import Mapeador
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.objetos_valor import ImagenEstandarizada, EstadoEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.dominio.entidades import ProcesoEstandarizacion
from datetime import date


class MapeadorProcesoEstandarizacionDTOJson(AppMap):

    def externo_a_dto(self, externo: dict) -> ProcesoEstandarizacionDTO:
        proceso_estandarizacion_dto = ProcesoEstandarizacionDTO()
        proceso_estandarizacion_dto.id_proceso_ingestion = externo.get('id_proceso_ingestion')
        proceso_estandarizacion_dto.id = externo.get('id')
        proceso_estandarizacion_dto.fecha_creacion = str(date.today())
        proceso_estandarizacion_dto.estado = externo.get('estado', 'PENDIENTE')
        imagenes: list[ImagenEstandarizadaDTO] = list()

        for imagen in externo.get('imagenes', list()):
            imagen_dto: ImagenEstandarizadaDTO = ImagenEstandarizadaDTO(
                imagen.get('tipo'),
                imagen.get('archivo'),
                imagen.get('archivo_estandarizado')
            )
            proceso_estandarizacion_dto.imagenes.append(imagen_dto)

        return proceso_estandarizacion_dto

    def dto_a_externo(self, dto: ProcesoEstandarizacionDTO) -> dict:
        return dto.__dict__


class MapeadorProcesoEstandarizacion(RepMap):
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

        imagenes_dto: list[ImagenEstandarizadaDTO] = dto.imagenes
        for imagen_dto in imagenes_dto:
            imagen = ImagenEstandarizada(
                tipo=imagen_dto.tipo,
                archivo=imagen_dto.archivo,
                archivo_estandarizado=imagen_dto.archivo_estandarizado
            )
            proceso_estandarizacion.imagenes.append(imagen)

        return proceso_estandarizacion
