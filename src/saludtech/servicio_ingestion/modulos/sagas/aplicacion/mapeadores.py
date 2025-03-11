import uuid
from datetime import datetime
import ast
from saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion.dto import ImagenAnonimizadaDTO
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.comandos.anonimizacion import AnonimizarProceso
from saludtech.servicio_ingestion.modulos.sagas.aplicacion.comandos.estandarizacion import ProcesarEstandarizacion
class MapeadorSagas():

    def evento_a_anonimizacion(self,evento):
            fecha_creacion = datetime.fromtimestamp(evento.fecha_creacion / 1000.0).strftime('%Y-%m-%d')
            id_proceso = str(uuid.uuid4())
            imagenes= ast.literal_eval(evento.imagenes)
            imagenes_comando:list[ImagenAnonimizadaDTO] = list()
            for imagen in imagenes:
                imagen_dto: ImagenAnonimizadaDTO = ImagenAnonimizadaDTO(tipo=imagen.get('tipo'),archivo=imagen.get('archivo'),archivo_original=imagen.get('archivo'))
                imagenes_comando.append(imagen_dto)
            
            
            comando = AnonimizarProceso(
                fecha_creacion=fecha_creacion,
                fecha_actualizacion=fecha_creacion,
                id=id_proceso,
                imagenes=imagenes_comando,
                id_proceso_original=evento.id_proceso_ingestion
            )
            return comando
    
    def evento_a_estandarizacion(self,evento):
        fecha_creacion=datetime.fromtimestamp(evento.fecha_creacion / 1000.0).strftime('%Y-%m-%d')
        id_proceso_ingestion= str(evento.id_proceso_original)
        id_proceso = str(uuid.uuid4())
        imagenes= ast.literal_eval(evento.imagenes)
        imagenes_comando:list[ImagenEstandarizadaDTO] = list()
        for imagen in imagenes:
                imagen_dto: ImagenEstandarizadaDTO = ImagenEstandarizadaDTO(tipo=imagen.get('tipo'),archivo=imagen.get('archivo'),archivo_estandarizado=True)
                imagenes_comando.append(imagen_dto)
        comando= ProcesarEstandarizacion(
            fecha_creacion= fecha_creacion,
            id= id_proceso,
            imagenes= imagenes_comando,
            id_proceso_ingestion= id_proceso_ingestion
        )
        return comando
  