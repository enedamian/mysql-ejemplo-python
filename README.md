# mysql-ejemplo-python

Repositorio educativo: ejemplo de API REST con Flask y MySQL.

Este proyecto está pensado como referencia para alumnos que deban practicar:
- Conexión a MySQL desde Python (`mysql-connector-python`).
- Uso de un pool de conexiones centralizado.
- Organización por capas: entidades, repositorios, rutas (endpoints).
- Pruebas locales con un script SQL de seed.

Contenido del repositorio (resumen)
- `app.py` : arranque de la app Flask y registro de blueprints.
- `requirements.txt` : dependencias del proyecto.
- `db/` : scripts y utilidades de base de datos
  - `db.sql` : script para crear la base de datos de ejemplo y tablas.
  - `conexion.py` : gestión del pool de conexiones (clase `Conexion`).
  - `test_conexion.py` : script que prueba la obtención/uso del pool.
- `modelos/entidades/` : clases de dominio (por ejemplo `Producto`).
- `modelos/repositorios/` : clases que implementan el acceso a datos (CRUD).
- `rutas/` : blueprints y endpoints de la API.

Cómo preparar el entorno
1. Crear y activar un entorno virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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
- `db/conexion.py`: centraliza la configuración y entrega conexiones (pool). Todos los repositorios deben pedir la conexión aquí para evitar duplicar configuración.
- `modelos/entidades`: validaciones y lógica ligera de dominio. Crear/validar objetos antes de persistir.
- `modelos/repositorios`: encapsulan SQL y mapeo fila→entidad. Responsabilidad: abrir/cerrar conexiones (o usar un context manager central).
- `rutas`: exponen la API y traducen JSON↔entidades.

Buenas prácticas sugeridas para alumnos
- Validar datos en las entidades, no en los endpoints.
- Usar `with` o `try/finally` para asegurar `conn.close()` si se toma conexión manualmente.
- Mantener la `Conexion` como único lugar donde se gestiona pool/reintentos.
- No versionar `.env`, agregarlo en el `.gitignore` de los proyectos para evitar que se versione.

