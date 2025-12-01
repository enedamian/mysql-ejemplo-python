import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()  # Carga variables de entorno desde .env

class Conexion:
    __pool = None   # Pool compartido (atributo de clase)

    @classmethod
    def inicializar_pool(cls):
        if cls.__pool is None:
            cls.__pool = pooling.MySQLConnectionPool(
                pool_size=5,   # Número máximo de conexiones simultáneas
                pool_name="pool_api",
                pool_reset_session=True,
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME")
            )

    @classmethod
    def obtener_conexion(cls):
        if cls.__pool is None:
            cls.inicializar_pool()  # Crea el pool una sola vez
        return cls.__pool.get_connection() # Obtiene una conexión del pool
    

class TestConexion:
    @staticmethod
    def run_tests():
        print("=== PRUEBA DE CONEXIÓN A LA BASE DE DATOS CON POOL ===")
        conexion = Conexion.obtener_conexion()
        try:
            if conexion.is_connected():
                print("✓ Conexión exitosa a la base de datos MySQL desde el pool.")
            else:
                print("✗ No se pudo conectar a la base de datos MySQL desde el pool.")
        finally:
            if conexion.is_connected():
                print("Cerrando la conexión obtenida del pool...")
                conexion.close()
        print("Prueba de conexión finalizada.")
        print("==============================================='n")
        print("Testear limite de conexiones del pool...")
        conexiones = []
        try:
            for i in range(7):  # Intentar obtener más conexiones que el tamaño del pool
                print(f"Obteniendo conexión {i + 1}...")
                conn = Conexion.obtener_conexion()
                conexiones.append(conn)
                print(f"\033[92m Conexión {i + 1} obtenida.\033[0m")
        except Exception as e:
            print(f"\033[91m✗ Error al obtener una conexión: {e}\033[0m")
        finally:
            i=0
            for conn in conexiones:
                if conn.is_connected():
                    i+=1
                    print(f"\033[93mCerrando conexión {i}...\033[0m")
                    conn.close()


if __name__ == "__main__":
    TestConexion.run_tests()
    