from saludtech.servicio_estandarizacion.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioEstandarizacionExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de estandarizacion'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)