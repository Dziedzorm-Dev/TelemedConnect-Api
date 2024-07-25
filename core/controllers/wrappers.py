from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt

from core.models.session_token import SessionToken
from core.utils.utils_ import is_token_expired


def get_access_token():
    try:
        verify_jwt_in_request()
        token = request.headers.get('Authorization').split()[1]
        return token
    except Exception:
        return None


def valid_session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        user_id = get_jwt_identity()
        access_token = get_access_token()

        if access_token is None:
            return jsonify(result_flag={'value': 0, 'message': 'Not Authorisation token provided '}), 404

        session = SessionToken.query.filter_by(user_id=user_id, session_token=access_token).first()

        if not session:
            return jsonify(
                flag={'value': 0, 'message': 'Invalid session'}
            ), 404

        if not session.is_active:
            return jsonify(
                flag={'value': 0, 'message': 'Invalid session'}
            ), 404

        if is_token_expired(access_token):
            session.is_active = False
            session.delete()
            return jsonify(
                flag={'value': 0, 'message': 'Session is expired'}
            ), 403

        return f(*args, **kwargs)

    return decorated_function


def standard_session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        use = get_jwt().get('use', None)

        if use != "standard use":
            return jsonify(
                flag={'value': 0, 'message': 'You do not have permission to perform this operation'}
            ), 403

        return f(*args, **kwargs)

    return decorated_function

