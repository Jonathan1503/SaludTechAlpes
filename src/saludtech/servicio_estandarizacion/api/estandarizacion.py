import saludtech.servicio_estandarizacion.seedwork.presentacion.api as api
import json
from flask import redirect, render_template, request, session, url_for
from flask import Response
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.mapeadores import MapeadorProcesoEstandarizacionDTOJson
from saludtech.servicio_estandarizacion.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.dto import ProcesoEstandarizacionDTO
from saludtech.servicio_estandarizacion.seedwork.dominio.excepciones import ExcepcionDominio
from multiprocessing import Process
from saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.despachadores import Despachador
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.comandos.procesar_estandarizacion import ProcesarEstandarizacion
from saludtech.servicio_estandarizacion.modulos.estandarizacion.aplicacion.queries.obtener_proceso_estandarizacion import ObtenerProcesoEstandarizacion
from saludtech.servicio_estandarizacion.seedwork.aplicacion.queries import ejecutar_query
import saludtech.servicio_estandarizacion.modulos.estandarizacion.infraestructura.consumidores as estandarizacion

bp = api.crear_blueprint('estandarizacion', '/estandarizacion')


@bp.route('/estandarizacion-comando', methods=('POST',))
def proceso_estandarizacion_asincronica():
    try:
        proceso_estandarizacion_dict = request.json

        map_proceso_estandarizacion = MapeadorProcesoEstandarizacionDTOJson()
        proceso_estandarizacion_dto = map_proceso_estandarizacion.externo_a_dto(proceso_estandarizacion_dict)

        comando = ProcesarEstandarizacion(proceso_estandarizacion_dto.fecha_creacion,
                                        proceso_estandarizacion_dto.fecha_actualizacion,
                                        proceso_estandarizacion_dto.id,
                                        proceso_estandarizacion_dto.imagenes,
                                        proceso_estandarizacion_dto.id_proceso_ingestion,
                                        proceso_estandarizacion_dto.estado)

        hp1 = Process(target=estandarizacion.suscribirse_a_eventos, daemon=True).start()
        hp2 = Process(target=estandarizacion.suscribirse_a_comandos, daemon=True).start()

        despachador = Despachador()
        despachador.publicar_comando(comando, 'comandos-proceso_estandarizacion')

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/proceso-estandarizacion-query', methods=('GET',))
@bp.route('/proceso-estandarizacion-query/<id>', methods=('GET',))
def dar_proceso_estandarizacion(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerProcesoEstandarizacion(id))
        map_proceso_estandarizacion = MapeadorProcesoEstandarizacionDTOJson()

        return map_proceso_estandarizacion.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]
