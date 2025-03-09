import os
from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import saludtech.servicio_anonimizacion.modulos.anonimizacion.aplicacion

def importar_modelos_alchemy():
    import saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.dto

def comenzar_consumidor(app):
    import threading
    import saludtech.servicio_anonimizacion.modulos.anonimizacion.infraestructura.consumidores as anonimizacion
    threading.Thread(target=anonimizacion.suscribirse_a_eventos, args=(app,)).start()
    threading.Thread(target=anonimizacion.suscribirse_a_comandos, args=(app,)).start()

def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 
        "postgresql://postgres:password@postgres-db-anom:5434/anonimizacion"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 1
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 300
    app.secret_key = 'abc'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')
    
    from saludtech.servicio_anonimizacion.config.db import init_db
    init_db(app)
    
    from saludtech.servicio_anonimizacion.config.db import db
    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error al crear las tablas: {e}")
            raise

        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    from . import anonimizacion
    app.register_blueprint(anonimizacion.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Anonimización API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app