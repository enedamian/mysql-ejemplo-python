from mysql.connector import Error
from modelos.entidades.producto import Producto
#from modelos.conexion import Conexion
from db.conexion import Conexion


class RepositorioProductos:
    """CRUD de productos."""

    def obtener_todos(self) -> list[Producto]:
        """
        Obtiene todos los productos de la base de datos.
        
        Returns:
            Lista de objetos Producto (todos con ID asignado)
        """
                
        try:
            conexion = Conexion().obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, precio, descripcion, stock FROM productos")
            # Obtenemos todas las filas devueltas por la consulta
            filas = cursor.fetchall()
            productos = []
            for fila in filas:
                #print(fila)  # Para debug: muestra cada fila obtenida
                diccionario = {
                    "id": fila["id"],
                    "nombre": fila["nombre"],
                    "precio": float(fila["precio"]), # Los campos DECIMAL de MySQL debemos convertirlos a float
                    "descripcion": fila["descripcion"],
                    "stock": fila["stock"]
                }
                productos.append(Producto.from_dict(diccionario))
            cursor.close()
            conexion.close()
            return productos
        except Error as e:
            raise Exception(f"Error al obtener productos: {e}")
        

    
    def obtener_por_id(self, id: int) -> Producto|None:
        """
        Obtiene un producto por su ID.
        
        Args:
            id: ID del producto a buscar
            
        Returns:
            Objeto Producto si existe, None si no se encuentra
        """
        try:
            conexion = Conexion().obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            # armamos la consulta SQL con un placeholder para el ID (parametrizado)
            sql = "SELECT id, nombre, precio, descripcion, stock FROM productos WHERE id = %s"
            # ejecutamos la consulta pasando el ID como parámetro
            cursor.execute(sql, [id])
            fila = cursor.fetchone() # obtenemos una sola fila (porque sabemos que el ID es único) o None si no existe
            
            if fila:
                diccionario = {
                    "id": fila["id"],
                    "nombre": fila["nombre"],
                    "precio": float(fila["precio"]), # Convertir DECIMAL a float
                    "descripcion": fila["descripcion"],
                    "stock": fila["stock"]
                }
                return Producto.from_dict(diccionario)
            cursor.close()
            conexion.close()
            return None
        except Error as e:
            raise Exception(f"Error al obtener producto con ID {id}: {e}")
    
    def agregar(self, nuevo: Producto):
        """
        Crea un nuevo producto en la base de datos.
        
        Args:
            datos: Diccionario con los datos del producto (nombre, precio, descripcion, stock)
                   NO debe incluir 'id' (se genera automáticamente)
        
        Returns:
            Objeto Producto con el ID asignado por MySQL
            
        """
        try:
            conexion=Conexion().obtener_conexion()
            cursor = conexion.cursor()
            # Preparamos la consulta parametrizada SQL para insertar un nuevo producto
            sql = (
                "INSERT INTO productos (nombre, precio, descripcion, stock) "
                "VALUES (%s, %s, %s, %s)"
            )
            # Preparamos los parámetros para la consulta en una tupla: (param1, param2, ...)
            parametros = (
                nuevo.obtener_nombre(),
                nuevo.obtener_precio(),
                nuevo.obtener_descripcion(),
                nuevo.obtener_stock()
            )
            cursor.execute(sql, parametros)
            conexion.commit()
            id_generado = cursor.lastrowid
            nuevo.establecerId(id_generado)
            cursor.close()
            conexion.close()
            return nuevo
        except Error as e:
            raise Exception(f"Error al crear producto: {e}")
        
    
    def actualizar(self, producto_id:int, datos:dict) -> bool:
        """
        Actualiza un producto existente.
        
        Args:
            producto_actualizado: Objeto Producto con los datos actualizados
        
        Returns:
            True si se actualizó correctamente, False si no existe el producto
        
        """
        producto_actualizado = self.obtener_por_id(producto_id)
        #actualizamos los valores nuevos en el producto obtenido
        if producto_actualizado:
            try:
                # Actualizamos los valores del producto con los datos proporcionados
                if "nombre" in datos:
                    producto_actualizado.establecer_nombre(datos["nombre"])
                if "precio" in datos:
                    producto_actualizado.establecer_precio(datos["precio"])
                if "descripcion" in datos:
                    producto_actualizado.establecer_descripcion(datos["descripcion"])
                if "stock" in datos:
                    producto_actualizado.establecer_stock(datos["stock"])
                
                # ahora que el objeto está actualizado, guardamos los cambios en la base de datos
                # Preparamos la consulta SQL parametrizada para actualizar el producto
                sql = "UPDATE productos SET nombre = %s, precio = %s, descripcion = %s, stock = %s WHERE id = %s"
                parametros = (
                    producto_actualizado.obtener_nombre(),
                    producto_actualizado.obtener_precio(),
                    producto_actualizado.obtener_descripcion(),
                    producto_actualizado.obtener_stock(),
                    producto_actualizado.obtener_id()
                )
                conexion=Conexion().obtener_conexion()
                cursor = conexion.cursor()
                cursor.execute(sql, parametros)
                conexion.commit()
                cursor.close()
                conexion.close()
                return cursor.rowcount > 0 # devuelve True si 1>0. rowcount indica la cantidad de filas afectadas
            except Error as e:
                raise Exception(f"Error al actualizar producto con ID {id}: {e}")
        else:
            return False
    
    def eliminar(self, id: int) -> bool:
        """
        Elimina un producto de la base de datos.
        
        Args:
            id: ID del producto a eliminar
        
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        try:
            conexion=Conexion().obtener_conexion()
            cursor = conexion.cursor()
            # Preparamos la consulta SQL parametrizada para eliminar el producto
            sql = "DELETE FROM productos WHERE id = %s"
            # Ejecutamos la consulta pasando el ID como parámetro
            cursor.execute(sql, [id])
            conexion.commit()
            cursor.close()
            conexion.close()
            return cursor.rowcount > 0
        except Error as e:
            raise Exception(f"Error al eliminar producto con ID {id}: {e}")
