from flask import Blueprint, request, jsonify
from models.conexion import conectar

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()
    conn.close()
    return jsonify(datos)

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO usuarios (nombre, rol) VALUES (%s, %s)"
    cursor.execute(sql, (data['nombre'], data['rol']))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Usuario creado"})