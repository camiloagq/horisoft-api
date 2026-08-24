from flask import Blueprint, request, jsonify
from models.conexion import conectar

pqrs_bp = Blueprint('pqrs', __name__)


# GET /pqrs/
@pqrs_bp.route('/', methods=['GET'])
def obtener_pqrs():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pqrs")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


# GET /pqrs/<id>
@pqrs_bp.route('/<int:id>', methods=['GET'])
def obtener_pqr(id):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM pqrs WHERE id = %s",
        (id,)
    )

    dato = cursor.fetchone()

    cursor.close()
    conn.close()

    if dato:
        return jsonify(dato)

    return jsonify({
        "mensaje": "PQRS no encontrada"
    }), 404


# POST /pqrs/
@pqrs_bp.route('/', methods=['POST'])
def crear_pqr():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO pqrs
        (usuario_id, tipo, asunto, descripcion, estado)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['usuario_id'],
            data['tipo'],
            data['asunto'],
            data['descripcion'],
            data['estado']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "PQRS registrada correctamente",
        "id": nuevo_id
    }), 201


# PUT /pqrs/<id>
@pqrs_bp.route('/<int:id>', methods=['PUT'])
def actualizar_pqr(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE pqrs
        SET estado = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['estado'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "PQRS actualizada correctamente"
    })


# DELETE /pqrs/<id>
@pqrs_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_pqr(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pqrs WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "PQRS eliminada correctamente"
    })