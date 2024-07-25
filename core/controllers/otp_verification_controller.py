from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from core.controllers.wrappers import valid_session_required
from core.helpers.auth_helpers import verify_otp_helper, resend_otp_helper

otp_verification_bp = Blueprint('otp', __name__)


@otp_verification_bp.route('auth/verify', methods=['POST'], endpoint='verify_otp')
@jwt_required()
@valid_session_required
def verify_otp():
    data = request.json
    otp_token = data.get('otp_token', None)
    otp_code = data.get('otp_code', None)
    user_id = get_jwt_identity()
    use = get_jwt().get('use', None)
    role = get_jwt().get('role', None)

    return verify_otp_helper(user_id, otp_token, otp_code, use, role)


@otp_verification_bp.route('auth/resend', methods=['POST'], endpoint='resend_otp')
@jwt_required()
@valid_session_required
def resend_otp():
    data = request.get_json()
    otp_token = data.get('otp_token', None)
    email = data.get('email', None)
    user_id = get_jwt_identity()

    return resend_otp_helper(user_id, email, otp_token)

