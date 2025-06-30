import time
from tablero import Tablero
from jugador import Jugador
from config import ConfigManager


"""
Clase que se encarga de llevar a cabo el juego
"""
class Juego:
    def __init__(self):
        self.jugador = None
        self.tablero = None
        self.config = ConfigManager()
    
    def iniciar_juego(self):
        """ Iniciar el juego """
        print("¡Bienvenido al Buscaminas UNIMET!")
        nombres = input("Por favor ingresa tu nombre: ").split(" ")
        nombre = nombres[0]
        # Dejar el apellido en blanco si no lo proporcionó
        if len(nombres) == 1:
            apellido = " "
        else:
            apellido = nombres[1]
        # Crear un nuevo jugador y pedir el archivo de configuración
        self.jugador = Jugador(nombre, apellido)
        print("")
        print("---")
        print("Para comenzar, indica el nombre del archivo con la configuración del juego.")
        print("De lo contrario, presiona ENTER para consultar la API.")
        path = input("Escribe el nombre o presiona ENTER: ")
        self.config.cargar_configuracion(path)
        # Seguir pidiendo input hasta que el usuario decida salir
        while True:
            print("")
            print("--- MENÚ PRINCIPAL ---")
            print("1. Nueva partida")
            print("2. Ver records")
            print("3. Salir")
            opcion = input("Ingresa una opción: ")
            # Revisar la opción dada y actuar
            if opcion == '1':
                self.nueva_partida()
            elif opcion == '2':
                self.mostrar_records()
            elif opcion == '3':
                print("¡Gracias por jugar! Hasta luego.")
                break
            # Seguir pidiendo opciones si no ingresó una válida
            else:
                print("Opción no válida. Intenta de nuevo.")
    
    def nueva_partida(self):
        """ Iniciar una nueva partida """
        self.tablero = Tablero(self.config.filas, self.config.columnas, self.config.minas)
        self.jugador.iniciar_timer()
        print(f"Nueva partida - Tablero {self.config.filas}x{self.config.columnas} con {self.config.minas} minas")
        # Seguir pidiendo acciones al usuario hasta que el juego termine
        while not self.tablero.juego_terminado:
            self.mostrar_estado_juego()
            self.procesar_accion()
        # Mostrar el resultado final al terminar
        self.mostrar_resultado_final()
    
    def mostrar_estado_juego(self):
        """ Mostrar el estado actual del juego """
        tiempo_transcurrido = int(time.time() - self.jugador.tiempo_inicio)
        # Minas restantes es las minas totales menos las que se han marcado con bandera
        minas_restantes = self.config.minas - sum(
            1 for fila in self.tablero.casillas 
            for casilla in fila 
            if casilla.marca == "bandera"
        )
        print(f"Tiempo: {tiempo_transcurrido} segundos - Minas restantes: {minas_restantes}")
        self.tablero.mostrar_tablero()
    
    def procesar_accion(self):
        """ Procesar una acción del jugador """
        while True:
            print("")
            print("Escoge una acción de las siguientes:")
            print("r [fila] [columna] - Revelar casilla")
            print("b [fila] [columna] - Colocar/quitar bandera")
            print("i [fila] [columna] - Colocar/quitar interrogante")
            print("s - Salir al menú principal")
            entrada = input("Ingresa una acción: ").strip().split()
            if not entrada:
                continue
            comando = entrada[0].lower()
            # Terminar el juego y salir al menú principal
            if comando == 's':
                self.tablero.juego_terminado = True
                return
            # Revelar o marcar con bandera o interrogante una casilla
            if comando in ('r', 'b', 'i') and len(entrada) == 3:
                try:
                    fila = int(entrada[1])
                    columna = int(entrada[2])
                    # Revelar una casilla
                    if comando == 'r':
                        # Verificar si encontró una mina
                        if self.tablero.revelar_casilla(fila, columna):
                            return
                        break
                    # Colocar/quitar una bandera
                    elif comando == 'b':
                        casilla = self.tablero.casillas[fila][columna]
                        tipo_marca = None if casilla.marca == "bandera" else "bandera"
                        self.tablero.marcar_casilla(fila, columna, tipo_marca)
                        break
                    # Colocar/quitar una interrogante
                    elif comando == 'i':
                        casilla = self.tablero.casillas[fila][columna]
                        tipo_marca = None if casilla.marca == "interrogante" else "interrogante"
                        self.tablero.marcar_casilla(fila, columna, tipo_marca)
                        break
                except (ValueError, IndexError):
                    pass
            print("Entrada no válida. Intenta de nuevo.")
    
    def mostrar_resultado_final(self):
        """ Mostrar el resultado final del juego """
        tiempo = self.jugador.detener_timer()
        self.tablero.mostrar_tablero()
        # Mensaje de felicidades si el jugador ganó
        if self.tablero.ganado:
            print(f"¡Felicidades {self.jugador.nombre}! ¡Ganaste!")
            print(f"Tiempo: {int(tiempo)} segundos")
            # Indicar si es nuevo récord
            if self.config.es_record(tiempo):
                print("¡Nuevo récord!")
                tamano = self.config.filas * self.config.columnas
                self.config.agregar_record(self.jugador.nombre, self.jugador.apellido, tiempo, tamano)
        # Pérdida del juego si se encontró una mina
        else:
            print("¡Boom! ¡Mina encontrada!")
    
    def mostrar_records(self):
        """ Mostrar los records almacenados """
        print("")
        print("--- MEJORES TIEMPOS ---")
        # Chequear que haya mejores tiempos
        if not self.config.records:
            print("No hay mejores tiempos registrados aún.")
            print("¡Sé el primero en alcanzar un record!")
            return
        # Imprimir los mejores tiempos
        for i, record in enumerate(self.config.records, 1):
            minutos = int(record["time"] // 60)
            segundos = int(record["time"] % 60)
            print(f"{i}. {record['first_name']} {record['last_name']} - {minutos}:{segundos:02d} (tamaño: {record['tamano']})")
