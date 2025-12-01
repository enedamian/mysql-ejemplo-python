from flask import Blueprint, jsonify, request
from modelos.entidades.producto import Producto
from modelos.repositorios.repositorio_productos import RepositorioProductos

productos_bp = Blueprint('productos', __name__)
repo = RepositorioProductos()

@productos_bp.route('/productos', methods=['GET'])
def listar_productos():
    # Lógica para listar productos
    productos = repo.obtener_todos()
    productos_dict = [p.to_dict() for p in productos]
    return jsonify(productos_dict), 200

@productos_bp.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    # Lógica para obtener un producto por ID
    producto = repo.obtener_por_id(producto_id)
    if producto:
        return jsonify(producto.to_dict()), 200
    return jsonify({"error": "Producto no encontrado"}), 404

@productos_bp.route('/productos', methods=['POST'])
def crear_producto():
    # Lógica para crear un nuevo producto
    if request.is_json:
        datos = request.get_json()
        try:
            nuevo_producto = Producto.from_dict(datos)
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        nuevo_producto = repo.agregar(nuevo_producto)
        if nuevo_producto.obtener_id() is not None:
            return jsonify({"mensaje": "producto agregado", "producto": nuevo_producto.to_dict()}), 201
        return jsonify({"error": "Error al crear el producto"}), 400
    else:
        return jsonify({"error": "Solicitud debe ser JSON"}), 415
    
@productos_bp.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    # Lógica para actualizar un producto existente
    if request.is_json:
        datos = request.get_json()
                
        exito = repo.actualizar(producto_id, datos)
        if exito:
            return jsonify({"mensaje": "Producto actualizado"}), 200
        return jsonify({"error": "Producto no encontrado"}), 404
    else:
        return jsonify({"error": "Solicitud debe ser JSON"}), 415
    
@productos_bp.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    # Lógica para eliminar un producto
    exito = repo.eliminar(producto_id)
    if exito:
        return jsonify({"mensaje": "Producto eliminado"}), 200
    return jsonify({"error": "Producto no encontrado"}), 404