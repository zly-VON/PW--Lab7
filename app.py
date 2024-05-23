from flask import Flask
from models.database import db
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    import routes
    app.config['JWT_SECRET_KEY'] = 'secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
    jwt = JWTManager(app)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'App Name': 'Gym Workout API'}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    
    app.run(debug=True)
