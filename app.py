from flask import Flask
from config import Config
from models import db
from controllers import controllers_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register combined controllers Blueprint
app.register_blueprint(controllers_bp)

if __name__ == '__main__':
    app.run(debug=True)

