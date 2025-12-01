import sys
import os

# para ejecutar pruebas desde esta ruta debemos agregar el path del proyecto al sys.path
# porque sino no encuentra el módulo db.conexion desde esta ubicación

# Obtiene la ruta del directorio actual del script (tests/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Obtiene la ruta del directorio padre (proyecto/)
parent_dir = os.path.dirname(current_dir)
# Agrega el directorio padre al path de busqueda
sys.path.append(parent_dir)

from db.conexion import Conexion
from time import sleep
from colorama import Fore, Style, init

class TestConexion:

    @staticmethod
    def run_tests():
        
        import colorama
        print(colorama.Fore.CYAN + "\n=== PRUEBA DE CONEXIÓN A LA BASE DE DATOS CON POOL ===\n" + colorama.Style.RESET_ALL)
        conexion = Conexion.obtener_conexion()
        try:
            if conexion.is_connected():
                print(colorama.Fore.GREEN + "✓ Conexión exitosa a la base de datos MySQL desde el pool." + colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.RED + "✗ No se pudo conectar a la base de datos MySQL desde el pool." + colorama.Style.RESET_ALL)
        finally:
            if conexion.is_connected():
                print("Cerrando la conexión obtenida del pool...")
                conexion.close()
        print(colorama.Fore.CYAN + "Prueba de conexión finalizada.\n" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "===============================================\n" + colorama.Style.RESET_ALL)
        print(colorama.Fore.LIGHTBLUE_EX + "Testear limite de conexiones del pool..." + colorama.Style.RESET_ALL)
        conexiones = []
        try:
            for i in range(7):  # Intentar obtener más conexiones que el tamaño del pool
                print( f"Obteniendo conexión {i + 1}..." )
                conn = Conexion.obtener_conexion()
                conexiones.append(conn)
                print(colorama.Fore.GREEN + f" Conexión {i + 1} obtenida." + colorama.Style.RESET_ALL)
        except Exception as e:
            print(colorama.Fore.RED + f"X Error al obtener una conexión: {e}" + colorama.Style.RESET_ALL)
        finally:
            i=0
            for conn in conexiones:
                if conn.is_connected():
                    i+=1
                    print(f"\033[93mCerrando conexión {i}...\033[0m")
                    conn.close()


if __name__ == "__main__":
    TestConexion.run_tests()