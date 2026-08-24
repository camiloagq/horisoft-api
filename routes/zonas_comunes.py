from flask import Blueprint, request, jsonify
from models.conexion import conectar

zonas_comunes_bp = Blueprint('zonas_comunes', __name__)


@zonas_comunes_bp.route('/', methods=['GET'])
def obtener_zonas():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM zonas_comunes")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


@zonas_comunes_bp.route('/', methods=['POST'])
def crear_zona():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO zonas_comunes
        (nombre, descripcion, capacidad, estado)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['nombre'],
            data['descripcion'],
            data['capacidad'],
            data['estado']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Zona común creada correctamente",
        "id": nuevo_id
    }), 201


@zonas_comunes_bp.route('/<int:id>', methods=['PUT'])
def actualizar_zona(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE zonas_comunes
        SET nombre = %s,
            descripcion = %s,
            capacidad = %s,
            estado = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['nombre'],
            data['descripcion'],
            data['capacidad'],
            data['estado'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Zona común actualizada correctamente"
    })


@zonas_comunes_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_zona(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM zonas_comunes WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Zona común eliminada correctamente"
    })