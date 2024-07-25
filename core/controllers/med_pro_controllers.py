from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from core.helpers.auth_helpers import sign_up_helper, sign_in_helper
from core.models.medical_record import MedicalRecord

med_pro_bp = Blueprint('med-pro', __name__)


@med_pro_bp.route('auth/sign-up', methods=['POST'], endpoint='sign_up')
def sign_up():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)
    return sign_up_helper(email, password, 3)


@med_pro_bp.route('auth/sign-in', methods=['POST'], endpoint='sign_in')
def sign_in():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)
    return sign_in_helper(email, password, 3)


@med_pro_bp.route('/medical-record/create', methods=['POST'], endpoint='create_medical_record')
def create_medical_record():
    doctor_id = get_jwt_identity()
    data = request.get_json()

    fields = [
        "patient_id",
        "diagnosis",
        "previous_consultation",
        "symptoms",
        "first_aid",
        "blood_pressure",
        "heart_rate",
        "respiratory_rate",
        "temperature",
        "oxygen_saturation"
    ]

    required = [
        "patient_id",
        "diagnosis",
        "previous_consultation"
        "symptoms",
        "diagnosis"
    ]

    record = MedicalRecord(doctor_id=doctor_id)
    for field in fields:
        if field in required and (field not in data.keys() or data[field] is None):
            return jsonify(
                flag={'value': 0, 'message': "{} not provided".format(field)}
            ), 403

        setattr(record, field, data[field])

    record.create()
    return jsonify(
        flag={'value': 0, 'message': "Medical record created successfully"}
    ), 403
