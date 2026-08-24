from flask import Blueprint, request, jsonify
from models.conexion import conectar

vehiculos_bp = Blueprint('vehiculos', __name__)


# GET /vehiculos/
@vehiculos_bp.route('/', methods=['GET'])
def obtener_vehiculos():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vehiculos")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


# GET /vehiculos/<id>
@vehiculos_bp.route('/<int:id>', methods=['GET'])
def obtener_vehiculo(id):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM vehiculos WHERE id = %s",
        (id,)
    )

    vehiculo = cursor.fetchone()

    cursor.close()
    conn.close()

    if vehiculo:
        return jsonify(vehiculo)

    return jsonify({
        "mensaje": "Vehículo no encontrado"
    }), 404


# POST /vehiculos/
@vehiculos_bp.route('/', methods=['POST'])
def crear_vehiculo():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO vehiculos
        (usuario_id, placa, marca, modelo, color, tipo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['usuario_id'],
            data['placa'],
            data['marca'],
            data['modelo'],
            data['color'],
            data['tipo']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Vehículo registrado correctamente",
        "id": nuevo_id
    }), 201


# PUT /vehiculos/<id>
@vehiculos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_vehiculo(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE vehiculos
        SET placa = %s,
            marca = %s,
            modelo = %s,
            color = %s,
            tipo = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['placa'],
            data['marca'],
            data['modelo'],
            data['color'],
            data['tipo'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Vehículo actualizado correctamente"
    })


# DELETE /vehiculos/<id>
@vehiculos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_vehiculo(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM vehiculos WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Vehículo eliminado correctamente"
    })