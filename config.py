import requests


# Constante: dirección de la API
DIRECCION_API = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main"


"""
Clase que se encarga del I/O de archivos y consultar la API
"""
class ConfigManager:
    def __init__(self):
        self.filas = 0
        self.columnas = 0
        self.minas = 0
        self.records = []
        self.archivo_config = ""
    
    def cargar_configuracion(self, archivo_config):
        """ Cargar la configuración desde el archivo """
        if not archivo_config:
            self._consultar_API()
            self.archivo_config = "./nueva_config.txt"
        else:
            self.archivo_config = archivo_config
            with open(self.archivo_config, 'r') as f:
                lineas = f.readlines()
                for linea in lineas:
                    linea = linea.strip()
                    if linea.startswith('filas='):
                        self.filas = int(linea.split('=')[1])
                    elif linea.startswith('columnas='):
                        self.columnas = int(linea.split('=')[1])
                    elif linea.startswith('minas='):
                        self.minas = int(linea.split('=')[1])
                    elif linea.startswith('records='):
                        records_str = linea.split('=')[1]
                        if records_str:
                            self.records = [self._parsear_record(r) for r in records_str.split(',')]

    def guardar_configuracion(self):
        """ Guardar la configuración en el archivo """
        with open(self.archivo_config, 'w') as f:
            f.write(f"filas={self.filas}\n")
            f.write(f"columnas={self.columnas}\n")
            f.write(f"minas={self.minas}\n")
            records_str = ','.join(
                f"{r["first_name"]}|{r["last_name"]}|{r["time"]}|{r["tamano"]}'"
                for r in self.records
            )
            f.write(f'records={records_str}\n')

    def _parsear_record(self, record_str):
        """ Convertir un string de record a diccionario. Se usa al leer el archivo de texto """
        partes = record_str.split('|')
        return {
            "first_name": partes[0],
            "last_name": partes[1],
            "time": float(partes[2]),
            "tamano": partes[3]
        }
    
    def agregar_record(self, first_name, last_name, tiempo, tamano):
        """ Agregar un nuevo tiempo record al registro """
        nuevo_record = {
            "first_name": first_name,
            "last_name": last_name,
            "time": tiempo,
            "tamano": tamano
        }
        self.records.append(nuevo_record)
        # Ordenar por tiempo (menor es mejor)
        self.records.sort(key=lambda x: x["time"])
        # Mantener solo los 3 mejores
        self.records = self.records[:3]
        self.guardar_configuracion()
    
    def es_record(self, tiempo):
        """ Determinar si un tiempo califica como record """
        if len(self.records) < 3:
            return True
        return tiempo < self.records[-1]["time"]
    
    def _consultar_API(self):
        # Cargar la configuración del tablero
        config = self._fetch_API("/config.json")
        self.filas, self.columnas = config["global"]["board_size"]
        # Determinar el número de minas dependiendo del modo de juego
        densidades = config["global"]["quantity_of_mines"]
        print("Modos de juego disponibles:")
        for i, modo in enumerate(densidades):
            print(f"{i + 1}. {modo.upper()}")
        # Multiplicar la densidad de minas por el tamaño del tablero
        modo_de_juego = int(input("Selecciona una opción: "))
        densidad = list(densidades.values())[modo_de_juego]
        self.minas = (self.filas * self.columnas) * densidad
        # Obtener los records del leaderboard
        self.records = self._fetch_API("/leaderboard.json")
        for item in self.records:
            item["tamano"] = self.filas * self.columnas
        
    
    def _fetch_API(self, final):
        """ Hacer un request GET a la API """
        url_final = f"{DIRECCION_API}{final}"
        print(f"Haciendo GET a {final}...")
        try:
            response = requests.get(url_final)
            if response.status_code == 200:
                return response.json()
            else:
                print("Respuesta (texto):", response.text[:100])
        except Exception as e:
            print(f"Error al hacer GET a {final}: {e}")
