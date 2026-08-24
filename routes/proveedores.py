from flask import Blueprint, request, jsonify
from models.conexion import conectar

proveedores_bp = Blueprint('proveedores', __name__)


# GET /proveedores/
@proveedores_bp.route('/', methods=['GET'])
def obtener_proveedores():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM proveedores")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


# GET /proveedores/<id>
@proveedores_bp.route('/<int:id>', methods=['GET'])
def obtener_proveedor(id):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM proveedores WHERE id = %s",
        (id,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if proveedor:
        return jsonify(proveedor)

    return jsonify({
        "mensaje": "Proveedor no encontrado"
    }), 404


# POST /proveedores/
@proveedores_bp.route('/', methods=['POST'])
def crear_proveedor():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO proveedores
        (nombre, nit, telefono, correo, direccion)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['nombre'],
            data['nit'],
            data['telefono'],
            data['correo'],
            data['direccion']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Proveedor creado correctamente",
        "id": nuevo_id
    }), 201


# PUT /proveedores/<id>
@proveedores_bp.route('/<int:id>', methods=['PUT'])
def actualizar_proveedor(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE proveedores
        SET nombre = %s,
            nit = %s,
            telefono = %s,
            correo = %s,
            direccion = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['nombre'],
            data['nit'],
            data['telefono'],
            data['correo'],
            data['direccion'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Proveedor actualizado correctamente"
    })


# DELETE /proveedores/<id>
@proveedores_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_proveedor(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM proveedores WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Proveedor eliminado correctamente"
    })