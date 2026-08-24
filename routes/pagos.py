from flask import Blueprint, request, jsonify
from models.conexion import conectar

pagos_bp = Blueprint('pagos', __name__)


# GET /pagos/
# Obtener todos los pagos
@pagos_bp.route('/', methods=['GET'])
def obtener_pagos():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pagos")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


# GET /pagos/<id>
# Obtener un pago específico
@pagos_bp.route('/<int:id>', methods=['GET'])
def obtener_pago(id):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM pagos WHERE id = %s",
        (id,)
    )

    pago = cursor.fetchone()

    cursor.close()
    conn.close()

    if pago:
        return jsonify(pago)

    return jsonify({
        "mensaje": "Pago no encontrado"
    }), 404


# POST /pagos/
# Registrar un pago
@pagos_bp.route('/', methods=['POST'])
def crear_pago():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Debe enviar información"
        }), 400

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO pagos
        (usuario_id, valor, fecha, estado)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['usuario_id'],
            data['valor'],
            data['fecha'],
            data['estado']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Pago registrado correctamente",
        "id": nuevo_id
    }), 201


# PUT /pagos/<id>
# Actualizar un pago
@pagos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_pago(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE pagos
        SET valor = %s,
            fecha = %s,
            estado = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['valor'],
            data['fecha'],
            data['estado'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Pago actualizado correctamente"
    })


# DELETE /pagos/<id>
# Eliminar un pago
@pagos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_pago(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pagos WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Pago eliminado correctamente"
    })