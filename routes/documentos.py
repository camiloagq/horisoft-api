from flask import Blueprint, request, jsonify
from models.conexion import conectar

documentos_bp = Blueprint('documentos', __name__)


@documentos_bp.route('/', methods=['GET'])
def obtener_documentos():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM documentos")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


@documentos_bp.route('/', methods=['POST'])
def crear_documento():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO documentos
        (nombre, tipo, ruta, fecha)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['nombre'],
            data['tipo'],
            data['ruta'],
            data['fecha']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Documento registrado correctamente",
        "id": nuevo_id
    }), 201


@documentos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_documento(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM documentos WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Documento eliminado correctamente"
    })