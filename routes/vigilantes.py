from flask import Blueprint, request, jsonify
from models.conexion import conectar

vigilantes_bp = Blueprint('vigilantes', __name__)


@vigilantes_bp.route('/', methods=['GET'])
def obtener_vigilantes():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vigilantes")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


@vigilantes_bp.route('/', methods=['POST'])
def crear_vigilante():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO vigilantes
        (nombre, documento, telefono, turno, estado)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['nombre'],
            data['documento'],
            data['telefono'],
            data['turno'],
            data['estado']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Vigilante registrado correctamente",
        "id": nuevo_id
    }), 201


@vigilantes_bp.route('/<int:id>', methods=['PUT'])
def actualizar_vigilante(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE vigilantes
        SET nombre = %s,
            documento = %s,
            telefono = %s,
            turno = %s,
            estado = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['nombre'],
            data['documento'],
            data['telefono'],
            data['turno'],
            data['estado'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Vigilante actualizado correctamente"
    })


@vigilantes_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_vigilante(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM vigilantes WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Vigilante eliminado correctamente"
    })