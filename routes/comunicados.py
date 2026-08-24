from flask import Blueprint, request, jsonify
from models.conexion import conectar

comunicados_bp = Blueprint('comunicados', __name__)


# GET /comunicados/
@comunicados_bp.route('/', methods=['GET'])
def obtener_comunicados():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM comunicados")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


# POST /comunicados/
@comunicados_bp.route('/', methods=['POST'])
def crear_comunicado():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO comunicados
        (titulo, mensaje, fecha, estado)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['titulo'],
            data['mensaje'],
            data['fecha'],
            data['estado']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Comunicado creado correctamente",
        "id": nuevo_id
    }), 201


# PUT /comunicados/<id>
@comunicados_bp.route('/<int:id>', methods=['PUT'])
def actualizar_comunicado(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE comunicados
        SET titulo = %s,
            mensaje = %s,
            fecha = %s,
            estado = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['titulo'],
            data['mensaje'],
            data['fecha'],
            data['estado'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Comunicado actualizado correctamente"
    })


# DELETE /comunicados/<id>
@comunicados_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_comunicado(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM comunicados WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Comunicado eliminado correctamente"
    })