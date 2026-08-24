from flask import Flask, jsonify
from routes.login import login_bp
from routes.usuarios import usuarios_bp
from routes.pagos import pagos_bp
from routes.pqrs import pqrs_bp
from routes.comunicados import comunicados_bp
from routes.configuracion import configuracion_bp
from routes.cuentas_cobro import cuentas_cobro_bp
from routes.documentos import documentos_bp
from routes.inventario import inventario_bp
from routes.proveedores import proveedores_bp
from routes.reservas import reservas_bp
from routes.vehiculos import vehiculos_bp
from routes.vigilantes import vigilantes_bp
from routes.zonas_comunes import zonas_comunes_bp

app = Flask(__name__)

# Registro de rutas
app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(pagos_bp, url_prefix="/pagos")
app.register_blueprint(pqrs_bp, url_prefix="/pqrs")
app.register_blueprint(comunicados_bp, url_prefix="/comunicados")
app.register_blueprint(configuracion_bp, url_prefix="/configuracion")
app.register_blueprint(cuentas_cobro_bp, url_prefix="/cuentasCobro")
app.register_blueprint(documentos_bp, url_prefix="/documentos")
app.register_blueprint(inventario_bp, url_prefix="/inventario")
app.register_blueprint(proveedores_bp, url_prefix="/proveedores")
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(vehiculos_bp, url_prefix="/vehiculos")
app.register_blueprint(vigilantes_bp, url_prefix="/vigilantes")
app.register_blueprint(zonas_comunes_bp, url_prefix="/zonasComunes")

@app.route('/')
def home():
    return "API HORISOFT funcionando 🚀"

if __name__ == '__main__':
    app.run(debug=True)