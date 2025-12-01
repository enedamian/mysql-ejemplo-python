from typing import Optional

class Producto:
    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea un Producto desde un diccionario.
        Para productos que vienen de la BD (con id) o datos de una solicitud POST (sin id).
        """
        return cls(
            id=data.get("id"),  # Usa .get() para permitir None, porque devuelve None si "id" no está presente
            nombre=data["nombre"],
            precio=data["precio"],
            descripcion=data["descripcion"],
            stock=data["stock"]
        )

    
    def __init__(self, nombre: str, precio: float, descripcion: str, stock: int, id: Optional[int] = None):
        """
        Constructor de Producto.
        
        Args:
            nombre: Nombre del producto
            precio: Precio del producto
            descripcion: Descripción del producto
            stock: Cantidad en stock
            id: ID del producto (None para productos nuevos, asignado por BD al persistir)
        """
        # Validación del ID (solo si se proporciona)
        if id is not None and (not isinstance(id, int) or id < 0):
            raise ValueError("El ID debe ser un entero no negativo o None.")
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise ValueError("El nombre debe ser una cadena no vacía.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número no negativo.")
        if not isinstance(descripcion, str) or descripcion.strip() == "":
            raise ValueError("La descripción debe ser una cadena no vacía.")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock debe ser un entero no negativo.")
        
        self.__id = id
        self.__nombre = nombre
        self.__precio = precio
        self.__descripcion = descripcion
        self.__stock = stock

    def obtener_id(self) -> Optional[int]:
        """Retorna el ID del producto (None si no ha sido persistido aún)."""
        return self.__id
    
    def obtener_nombre(self) -> str:
        return self.__nombre
    
    def obtener_precio(self) -> float:
        return self.__precio

    def obtener_descripcion(self) -> str:
        return self.__descripcion

    def obtener_stock(self) -> int:
        return self.__stock

    def establecerId(self, id: int):
        if not isinstance(id, int) or id < 0:
            raise ValueError("El ID debe ser un entero no negativo.")
        self.__id = id

    def establecer_nombre(self, nombre: str):
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise ValueError("El nombre debe ser una cadena no vacía.")
        self.__nombre = nombre

    def establecer_precio(self, precio: float):
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número no negativo.")
        self.__precio = precio

    def establecer_descripcion(self, descripcion: str):
        if not isinstance(descripcion, str) or descripcion.strip() == "":
            raise ValueError("La descripción debe ser una cadena no vacía.")
        self.__descripcion = descripcion

    def establecer_stock(self, stock: int):
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock debe ser un entero no negativo.")
        self.__stock = stock

    def se_puede_vender(self, cantidad: int) -> bool:
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un entero no negativo.")
        return self.__stock >= cantidad

    def to_dict(self) -> dict:
        """Convierte el producto a un diccionario."""
        resultado = {
            "nombre": self.__nombre,
            "precio": self.__precio,
            "descripcion": self.__descripcion,
            "stock": self.__stock
        }
        # Solo incluir el ID si existe (producto ya almacenado en BD)
        if self.__id is not None:
            resultado["id"] = self.__id
        return resultado
    
    def esta_almacenado(self) -> bool:
        """Indica si el producto ya fue guardado en la BD (tiene ID asignado)."""
        return self.__id is not None