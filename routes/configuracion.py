from flask import Blueprint, request, jsonify
from models.conexion import conectar

configuracion_bp = Blueprint('configuracion', __name__)


# GET /configuracion/
@configuracion_bp.route('/', methods=['GET'])
def obtener_configuracion():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM configuracion")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


# PUT /configuracion/<id>
@configuracion_bp.route('/<int:id>', methods=['PUT'])
def actualizar_configuracion(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE configuracion
        SET nombre_conjunto = %s,
            direccion = %s,
            telefono = %s,
            correo = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['nombre_conjunto'],
            data['direccion'],
            data['telefono'],
            data['correo'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Configuración actualizada correctamente"
    })