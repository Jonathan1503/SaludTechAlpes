from __future__ import annotations

from dataclasses import dataclass, field
from saludtech.servicio_anonimizacion.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class Dato(ObjetoValor):
    tipo: str
    contenido: str
    anonimizado: bool = False
    
    def tipo(self) -> str:
        return self.tipo
        
    def contenido(self) -> str:
        return self.contenido
        
    def anonimizado(self) -> bool:
        return self.anonimizado