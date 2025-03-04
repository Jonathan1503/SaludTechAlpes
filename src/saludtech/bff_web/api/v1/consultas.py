
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    procesos_ingestion: typing.List[ProcesoIngestion] = strawberry.field(resolver=obtener_procesos_ingestion)