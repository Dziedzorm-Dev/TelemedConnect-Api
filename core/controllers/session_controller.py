from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from core.controllers.wrappers import valid_session_required
from core.helpers.auth_helpers import refresh_session_helper

session_bp = Blueprint('session', __name__)


@session_bp.route('auth/refresh', methods=['GET'], endpoint='refresh_session')
@jwt_required()
@valid_session_required
def refresh_session():
    data = request.json
    exp_time = data.get('exp_time', None)
    user_id = get_jwt_identity()
    use = get_jwt().get('use', None)
    role = get_jwt().get('role', None)

    return refresh_session_helper(user_id, exp_time, use, role)
