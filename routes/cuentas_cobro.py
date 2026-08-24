from flask import Blueprint, request, jsonify
from models.conexion import conectar

cuentas_cobro_bp = Blueprint('cuentas_cobro', __name__)


@cuentas_cobro_bp.route('/', methods=['GET'])
def obtener_cuentas():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cuentas_cobro")

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


@cuentas_cobro_bp.route('/', methods=['POST'])
def crear_cuenta():

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO cuentas_cobro
        (usuario_id, periodo, valor, fecha_vencimiento, estado)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['usuario_id'],
            data['periodo'],
            data['valor'],
            data['fecha_vencimiento'],
            data['estado']
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Cuenta de cobro creada correctamente",
        "id": nuevo_id
    }), 201


@cuentas_cobro_bp.route('/<int:id>', methods=['PUT'])
def actualizar_cuenta(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE cuentas_cobro
        SET valor = %s,
            fecha_vencimiento = %s,
            estado = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['valor'],
            data['fecha_vencimiento'],
            data['estado'],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Cuenta de cobro actualizada correctamente"
    })