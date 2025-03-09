from __future__ import annotations
from dataclasses import dataclass, field

import saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.objetos_valor as ov
from saludtech.servicio_anonimizacion.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionCreado
from saludtech.servicio_anonimizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
import uuid

@dataclass
class ProcesoAnonimizacion(AgregacionRaiz):
    id_partner: uuid.UUID = field(hash=True, default=None)
    datos: list[ov.Dato] = field(default_factory=list[ov.Dato])
    
    def crear_proceso_anonimizacion(self, proceso_anonimizacion: ProcesoAnonimizacion):
        self.id_partner = proceso_anonimizacion.id_partner
        self.datos = proceso_anonimizacion.datos

        # Anonimizar todos los datos
        for dato in self.datos:
            self.anonimizar_dato(dato)

        self.agregar_evento(ProcesoAnonimizacionCreado(id_proceso_anonimizacion=self.id, id_partner=self.id_partner, fecha_creacion=self.fecha_creacion, datos=self.datos))

    def anonimizar_dato(self, dato: ov.Dato):
        # Lógica de anonimización, se podría implementar diferentes estrategias según el tipo
        if dato.tipo == 'personal':
            dato.contenido = self._anonimizar_datos_personales(dato.contenido)
        elif dato.tipo == 'medico':
            dato.contenido = self._anonimizar_datos_medicos(dato.contenido)
        elif dato.tipo == 'financiero':
            dato.contenido = self._anonimizar_datos_financieros(dato.contenido)
        
        dato.anonimizado = True
        return dato
    
    def _anonimizar_datos_personales(self, contenido: str) -> str:
        # Implementación de anonimización para datos personales
        # Ejemplo: Ocultar parte del texto, reemplazar nombres, etc.
        return f"ANONIMIZADO_PERSONAL:{contenido[:5]}..."
    
    def _anonimizar_datos_medicos(self, contenido: str) -> str:
        # Implementación de anonimización para datos médicos
        return f"ANONIMIZADO_MEDICO:{contenido[:5]}..."
    
    def _anonimizar_datos_financieros(self, contenido: str) -> str:
        # Implementación de anonimización para datos financieros
        return f"ANONIMIZADO_FINANCIERO:{contenido[:5]}..."