from flask import Blueprint, request, jsonify
from models.conexion import conectar

reservas_bp = Blueprint('reservas', __name__)


# =====================================================
# GET /reservas/
# Obtener todas las reservas
# =====================================================

@reservas_bp.route('/', methods=['GET'])
def obtener_reservas():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT
            r.id,
            r.usuario_id,
            u.nombre AS usuario,
            r.zona_id,
            z.nombre AS zona,
            r.fecha,
            r.hora_inicio,
            r.hora_fin,
            r.estado,
            r.observaciones
        FROM reservas r
        INNER JOIN usuarios u
            ON r.usuario_id = u.id
        INNER JOIN zonas_comunes z
            ON r.zona_id = z.id
        ORDER BY r.fecha
    """

    cursor.execute(sql)

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(datos)


# =====================================================
# GET /reservas/<id>
# Obtener una reserva
# =====================================================

@reservas_bp.route('/<int:id>', methods=['GET'])
def obtener_reserva(id):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT
            r.id,
            r.usuario_id,
            u.nombre AS usuario,
            r.zona_id,
            z.nombre AS zona,
            r.fecha,
            r.hora_inicio,
            r.hora_fin,
            r.estado,
            r.observaciones
        FROM reservas r
        INNER JOIN usuarios u
            ON r.usuario_id = u.id
        INNER JOIN zonas_comunes z
            ON r.zona_id = z.id
        WHERE r.id = %s
    """

    cursor.execute(sql, (id,))

    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if reserva:
        return jsonify(reserva)

    return jsonify({
        "mensaje": "Reserva no encontrada"
    }), 404


# =====================================================
# POST /reservas/
# Crear reserva
# =====================================================

@reservas_bp.route('/', methods=['POST'])
def crear_reserva():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Debe enviar información"
        }), 400

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO reservas
        (
            usuario_id,
            zona_id,
            fecha,
            hora_inicio,
            hora_fin,
            estado,
            observaciones
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            data['usuario_id'],
            data['zona_id'],
            data['fecha'],
            data['hora_inicio'],
            data['hora_fin'],
            data.get('estado', 'Pendiente'),
            data.get('observaciones', '')
        )
    )

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Reserva creada correctamente",
        "id": nuevo_id
    }), 201


# =====================================================
# PUT /reservas/<id>
# Actualizar reserva
# =====================================================

@reservas_bp.route('/<int:id>', methods=['PUT'])
def actualizar_reserva(id):

    data = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE reservas
        SET fecha = %s,
            hora_inicio = %s,
            hora_fin = %s,
            estado = %s,
            observaciones = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            data['fecha'],
            data['hora_inicio'],
            data['hora_fin'],
            data['estado'],
            data.get('observaciones', ''),
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Reserva actualizada correctamente"
    })


# =====================================================
# DELETE /reservas/<id>
# Eliminar reserva
# =====================================================

@reservas_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_reserva(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reservas WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Reserva eliminada correctamente"
    })