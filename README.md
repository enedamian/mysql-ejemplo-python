# mysql-ejemplo-python

Repositorio educativo: ejemplo de API REST con Flask y MySQL.

Este proyecto está pensado como referencia para que prueben y practiquen:
- Conexión a MySQL desde Python (`mysql-connector-python`).
- Uso de un pool de conexiones centralizado.
- Organización por capas: entidades, repositorios, rutas (endpoints).
- Una vez creada la BD e implementada la API, pueden realizar las consultas con Postman, Insomnia o software similar.

Contenido del repositorio (resumen)
- `app.py` : arranque de la app Flask y registro de blueprints.
- `requirements.txt` : dependencias del proyecto.
- `db/` : scripts y utilidades de base de datos
  - `db.sql` : script para crear la base de datos de ejemplo y popular las tablas.
  - `conexion.py` : gestión del pool de conexiones (clase `Conexion`).
  - `test_conexion.py` : script que prueba la obtención/uso del pool.
- `modelos/entidades/` : clases de dominio (por ejemplo `Producto`).
- `modelos/repositorios/` : clases que implementan el acceso a datos (CRUD).
- `rutas/` : blueprints y endpoints de la API.

Cómo preparar el entorno
1. Crear y activar un entorno virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Crear el archivo `.env` en la raíz con los datos de conexión:

```
DB_HOST=localhost
DB_USER=api_tienda
DB_PASS=password_superseguro
DB_NAME=tienda_ejemplo_python
DB_PORT=3306
```

> Nota: **no uses comillas alrededor de los valores** (ejemplo correcto `DB_HOST=localhost`; ejemplo incorrecto `DB_HOST='localhost'`).

3. Ejecutar el script SQL para crear la base, con datos de ejemplo (desde tu cliente MySQL) y el usuario para que la api se conecte a MySQL:

```sql
SOURCE db/db.sql;
```

4. Ejecutar la API localmente:

```powershell
python app.py
```

Endpoints (ejemplo)
- `GET /productos` — listar productos
- `GET /productos/<id>` — obtener producto
- `POST /productos` — crear producto
- `PUT /productos/<id>` — actualizar producto
- `DELETE /productos/<id>` — eliminar producto

Descripción de responsabilidades
- `db/conexion.py`: centraliza la configuración y la gestión de conexiones a MySQL mediante un pool.
  Responsabilidades:
  - Cargar las variables de entorno necesarias para la conexión (host, usuario, contraseña, base, puerto).
  - Inicializar y mantener un pool de conexiones (lazy-init) centralizando la gestión de conexiones.
  - Proveer métodos como `inicializar_pool()`, `obtener_conexion()` y, preferiblemente, un context manager `conectar()`
    para usar `with Conexion.conectar() as conn:` y garantizar que la conexión se devuelve al pool automáticamente.
  - Manejar errores de inicialización y obtención de conexiones, y presentar mensajes claros (sin exponer secretos).
  - Facilitar futuras mejoras (pooling, retries, métricas) sin tocar los repositorios.
- `modelos/entidades`: validaciones y lógica ligera de dominio. Crear/validar objetos antes de persistir.
- `modelos/repositorios`: encapsulan SQL y mapean las filas de la base de datos a objetos del sistema. Responsabilidades: abrir/cerrar conexiones, ejecutar consultas parametrizadas para evitar SQL injection, mapear filas de la BD a instancias de entidades, manejar transacciones cuando una operacion requiere atomicidad (commit/rollback), y encapsular detalles SQL para los controladores/servicios no los conozcan.
- `rutas` (controladores): reciben peticiones HTTP, validan y transforman datos, llaman a los repositorios
  para realizar la lógica de negocio y devuelven las respuestas (JSON). Actúan como la capa de controladores de la API.

Buenas prácticas sugeridas:
- Validar datos en las entidades, no en los endpoints.

- Los repositorios deben pedir la conexión a `db.conexion.Conexion` (no crear conexiones locales).
- Preferir `Conexion.conectar()` en un `with` para evitar fugas de conexiones; si se usa `obtener_conexion()`, siempre cerrar la conexión en un `finally` o llamar a `conn.close()`.
- No duplicar la configuración de conexión en otros módulos; centralizar cambios en `db/conexion.py` y mantenerlo como único lugar donde se gestiona pool/reintentos.
- No versionar `.env`, agregarlo en el `.gitignore` de los proyectos para evitar que se versione.

