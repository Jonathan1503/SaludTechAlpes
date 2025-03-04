import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


INGESTION_ADDRESS = os.getenv("INGESTION_ADDRESS", default="localhost")


def obtener_procesos_ingestion(root) -> typing.List["ProcesoIngestion"]:
    procesos_ingestion_json = requests.get(f'http://{INGESTION_ADDRESS}:5000/ingestion/proceso-ingestion-query').json()
    procesos_ingestion = []

    for proceso in procesos_ingestion_json:
        procesos_ingestion.append(
            ProcesoIngestion(
                fecha_creacion=proceso.get("fecha_creacion", ""),
                fecha_actualizacion=proceso.get("fecha_actualizacion", ""),
                id=proceso.get("id", ""),
                imagenes=[
                    Imagen(tipo=img.get("tipo", ""), archivo=img.get("archivo", ""))
                    for img in proceso.get("imagenes", [])
                ],
                id_partner=proceso.get("id_partner", "")
            )
        )

    return procesos_ingestion

@strawberry.type
class Imagen:
    tipo: str
    archivo: str

@strawberry.type
class ProcesoIngestion:
    fecha_creacion: str 
    fecha_actualizacion: str 
    id: str
    imagenes: typing.List[Imagen]
    id_partner: str 

@strawberry.type
class ProcesoIngestionRespuesta:
    mensaje: str
    codigo: int

