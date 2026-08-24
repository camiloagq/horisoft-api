from flask import Blueprint, request, jsonify
from models.conexion import conectar

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/', methods=['GET'])
def obtener_inventario():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventario")
    datos = cursor.fetchall()
    conn.close()
    return jsonify(datos)

@inventario_bp.route('/', methods=['POST'])
def crear_producto():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO inventario (nombre, cantidad) VALUES (%s, %s)"
    cursor.execute(sql, (data['nombre'], data['cantidad']))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Producto agregado"})