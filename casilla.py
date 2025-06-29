"""
Clase que representa una casilla del tablero
"""
class Casilla:
    def __init__(self):
        self.oculta = True
        self.marca = None
        self.es_mina = False
        self.minas_adyacentes = 0
        self.explotada = False

    def revelar(self):
        """ Revelar la casilla """
        self.oculta = False
        return self.es_mina

    def marcar(self, tipo_marca):
        """ Marcar la casilla con bandera o interrogante """
        # Marcar si está oculta y retornar verdadero
        if self.oculta:
            # Marcar con None equivale a quitar la marca actual
            if tipo_marca in ["bandera", "interrogante", None]:
                self.marca = tipo_marca
                return True
        # De lo contrario, retornar falso
        return False
    
    def __str__(self):
        """ Mostrar la casilla como texto para cuando se imprima el tablero """
        if self.oculta:
            if self.marca == 'bandera':
                return '⚑'
            elif self.marca == 'interrogante':
                return '?'
            return '░'
        elif self.es_mina:
            return '💣' if self.explotada else '⚙'
        elif self.minas_adyacentes > 0:
            return str(self.minas_adyacentes)
        return ' '
