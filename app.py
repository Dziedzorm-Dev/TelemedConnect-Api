from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from config import Config
from flask_migrate import Migrate
from core.database import db
from core.controllers.patient_contollers import patient_bp
from core.controllers.med_pro_controllers import med_pro_bp
from core.controllers.otp_verification_controller import otp_verification_bp
from core.controllers.session_controller import session_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

base_url = '/telemedconnect/api'

home_bp = Blueprint('home', __name__, url_prefix=base_url)


@home_bp.route('', methods=['GET'])
def home():
    return "Welcome to TelemedConnect!!"


app.register_blueprint(home_bp, url_prefix=f'{base_url}/')
app.register_blueprint(session_bp, url_prefix=f'{base_url}/session')
app.register_blueprint(otp_verification_bp, url_prefix=f'{base_url}/otp')
app.register_blueprint(patient_bp, url_prefix=f'{base_url}/patient')
app.register_blueprint(med_pro_bp, url_prefix=f'{base_url}/med-pro')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000)
