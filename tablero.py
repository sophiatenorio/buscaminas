import random
from casilla import Casilla


"""
Clase que representa el tablero de juego
"""
class Tablero:
    def __init__(self, filas, columnas, minas):
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.casillas = [[Casilla() for _ in range(columnas)] for _ in range(filas)]
        self.casillas_reveladas = 0
        self.juego_terminado = False
        self.ganado = False
        self.primer_movimiento = True

    def inicializar_tablero(self, fila_inicial, columna_inicial):
        """ Colocar  las minas aleatoriamente, evitando la casilla inicial y sus adyacentes """
        # Las casillas adyacentes a la inicial no pueden llevar minas
        posiciones_seguras = self._obtener_posiciones_adyacentes(fila_inicial, columna_inicial)
        posiciones_seguras.append((fila_inicial, columna_inicial))
        posiciones_minas = []
        minas_colocadas = 0
        # Repetir hasta que se hayan colocado todas las minas
        while minas_colocadas < self.minas:
            # Generar una fila y columna aleatoria en el rango
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            # Chequear que no está en las posiciones seguras
            if (fila, columna) not in posiciones_seguras and (fila, columna) not in posiciones_minas:
                posiciones_minas.append((fila, columna))
                minas_colocadas += 1
        # Actualizar la matriz de las minas
        for fila, columna in posiciones_minas:
            self.casillas[fila][columna].es_mina = True
        # Ya no estamos en el primer movimiento
        self._calcular_minas_adyacentes()
        self.primer_movimiento = False

    def _calcular_minas_adyacentes(self):
        """ Calcular el número de minas adyacentes para cada casilla """
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if not self.casillas[fila][columna].es_mina:
                    minas = 0
                    for f, c in self._obtener_posiciones_adyacentes(fila, columna):
                        if self.casillas[f][c].es_mina:
                            minas += 1
                    self.casillas[fila][columna].minas_adyacentes = minas

    def _obtener_posiciones_adyacentes(self, fila, columna):
        """ Devolver las posiciones adyacentes a una casilla dada """
        adyacentes = []
        for f in range(max(0, fila - 1), min(self.filas, fila + 2)):
            for c in range(max(0, columna - 1), min(self.columnas, columna + 2)):
                if f != fila or c != columna:
                    adyacentes.append((f, c))
        return adyacentes

    def revelar_casilla(self, fila, columna):
        """ Intentar revelar una casilla, devuelve True si era una mina """
        # Chequear que sigamos en juego y la casilla sea válida
        if self.juego_terminado or not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            return False
        casilla = self.casillas[fila][columna]
        # Retornar falso si ya está revelada
        if not casilla.oculta:
            return False
        # Revisar si es el primer movimiento
        if self.primer_movimiento:
            self.inicializar_tablero(fila, columna)
        # Revisar si es mina
        if casilla.es_mina:
            casilla.explotada = True
            self.juego_terminado = True
            self.ganado = False
            self._revelar_todas_minas()
            return True
        # Revelar las casillas colindantes
        self._revelar_recursivo(fila, columna)
        # Verificar si ganó
        if self.casillas_reveladas == (self.filas * self.columnas - self.minas):
            self.juego_terminado = True
            self.ganado = True
        return False

    def _revelar_recursivo(self, fila, columna):
        """ Revelar casillas recursivamente cuando se encuentra una casilla vacía """
        # Parar si la fila y la columna están fuera del rango
        if not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            return
        casilla = self.casillas[fila][columna]
        # Parar si la casilla se ha revelado o es mina o tiene una bandera
        if not casilla.oculta or casilla.es_mina or casilla.marca == "bandera":
            return
        casilla.revelar()
        self.casillas_reveladas += 1
        # Si no hay minas adyacentes, revelar las adyacentes recursivamente
        if casilla.minas_adyacentes == 0:
            for f, c in self._obtener_posiciones_adyacentes(fila, columna):
                self._revelar_recursivo(f, c)

    def _revelar_todas_minas(self):
        """ Revelar todas las minas al perder el juego """
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.casillas[fila][columna].es_mina:
                    self.casillas[fila][columna].revelar()

    def marcar_casilla(self, fila, columna, tipo_marca):
        """ Marcar una casilla con bandera o interrogante """
        if self.juego_terminado or not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            return False
        return self.casillas[fila][columna].marcar(tipo_marca)

    def mostrar_tablero(self):
        """ Mostrar el tablero en la consola """
        # Encabezado de columnas
        print('   ' + ' '.join(f'{i:2}' for i in range(self.columnas)))
        # Imprimir el tablero
        for fila in range(self.filas):
            # Número de fila
            print(f"{fila:2} ", end="")
            # Contenido de las casillas
            for columna in range(self.columnas):
                print(f"{self.casillas[fila][columna]} ", end="")
            print()
