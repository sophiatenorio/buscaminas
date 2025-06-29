import time


"""
Clase que representa un jugador de buscaminas
"""
class Jugador:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.tiempo_inicio = 0.0
        self.tiempo_fin = 0.0
    
    def iniciar_timer(self):
        """ Inicia el timer para una partida """
        self.tiempo_inicio = time.time()
        self.tiempo_fin = 0.0
    
    def detener_timer(self):
        """ Detener el timer y devuelve el tiempo transcurrido """
        if self.tiempo_inicio == 0.0:
            return 0.0
        return time.time() - self.tiempo_inicio
