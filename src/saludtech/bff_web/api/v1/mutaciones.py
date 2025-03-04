import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_reserva(self, id_partner: str, id_proceso_ingestion: str, imagenes: List[Imagen] , info: Info) -> ProcesoIngestionRespuesta:
        print(f"ID Partner: {id_partner}, ID Proceso ingestion: {id_proceso_ingestion}")
        payload = dict(
            id_partner = id_partner,
            fecha_creacion = utils.time_millis(),
            fecha_actualizacion = utils.time_millis(),
            id_proceso_ingestion = id_proceso_ingestion, 
            imagenes = imagenes
        )
        comando = dict(
            data = payload
        )

        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comandos-proceso_ingestion", "public/default/comandos-proceso_ingestion")
        
        return ReservaRespuesta(mensaje="Procesando Mensaje", codigo=203)