import sys
import subprocess
from juego import Juego


def chequear_requerimientos():
    """ Chequear que se tenga el paquete requests """
    try:
        import requests
        return True
    except ImportError:
        # Preguntar al usuario si desea instalarlo
        instalar = input("¿Deseas instalarlo automáticamente? (s/n): ").strip().lower()
        if instalar in ('s', 'si', 'sí'):
            try:
                # Instalar requests usando pip
                subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
                print("El paquete 'requests' se instaló correctamente.")
                return True
            except Exception as e:
                print(f"Error al instalar 'requests': {e}")
                return False
        else:
            print("¡El programa no funcionará sin 'requests'!")
            return False


if __name__ == "__main__":
    # Verificar e instalar requests antes de continuar
    if not chequear_requerimientos():
        sys.exit(1)  # Termina el programa si no está instalado
    # Iniciar el juego de lo contrario
    juego = Juego()
    juego.iniciar_juego()
