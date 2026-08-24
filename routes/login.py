from flask import Blueprint, request, jsonify
from models.conexion import conectar

login_bp = Blueprint('login', __name__)


# =====================================================
# POST /login
# =====================================================
@login_bp.route('/', methods=['POST'])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Debe enviar datos"
        }), 400

    correo = data.get('correo')
    password = data.get('password')

    if not correo or not password:
        return jsonify({
            "error": "Correo y contraseña son obligatorios"
        }), 400

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT id, nombre, correo, rol, estado
        FROM usuarios
        WHERE correo = %s AND password = %s
    """

    cursor.execute(sql, (correo, password))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario": usuario
        }), 200

    return jsonify({
        "error": "Credenciales incorrectas"
    }), 401
login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['POST'])
def login():
    return jsonify({"mensaje": "login funcionando"})