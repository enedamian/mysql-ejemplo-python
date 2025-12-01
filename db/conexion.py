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
        try:
            return cls.__pool.get_connection()  # Obtiene una conexión del pool
        except Exception as e:
            raise RuntimeError(f'Error al obtener conexión del pool: {e}')

