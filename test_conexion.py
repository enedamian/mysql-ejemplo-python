from db.conexion import Conexion
from time import sleep

class TestConexion:
    @staticmethod
    def run_tests():
        print("=== PRUEBA DE MÉTODOS DE CONEXIÓN USANDO db/Conexion con POOL ===")
        db_conexion = Conexion()
        conn_pool = db_conexion.obtener_conexion()
        try:
            if conn_pool.is_connected():
                print("\033[92m✓ Conexión obtenida del pool exitosamente.\033[0m")
            else:
                print("\033[91m✗ No se pudo obtener una conexión del pool.\033[0m")
        finally:
            if conn_pool.is_connected():
                print("Cerrando la conexión del pool obtenida...")
                conn_pool.close()
        print("Pruebas de conexión finalizadas.")

if __name__ == "__main__":
    TestConexion.run_tests()