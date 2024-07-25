from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from core.controllers.wrappers import valid_session_required
from core.controllers.wrappers import standard_session_required
from core.helpers.auth_helpers import sign_in_helper, sign_up_helper
from core.helpers.accounts_helper import get_account_details_helper, update_account_helper, get_transactions_helper, \
    make_transaction_helper, get_appointments_helper, book_appointment_helper

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('auth/sign-up', methods=['POST'], endpoint='sign_up')
def sign_up():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)
    return sign_up_helper(email, password, 0)


@patient_bp.route('auth/sign-in', methods=['POST'], endpoint='sign_in')
def sign_in():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)
    return sign_in_helper(email, password, 0)


@patient_bp.route('ops/account/details', methods=['GET'], endpoint='get_account_details')
@jwt_required()
@valid_session_required
@standard_session_required
def get_account_details():
    user_id = get_jwt_identity()
    return get_account_details_helper(user_id)


@patient_bp.route('ops/account/update', methods=['PUT'], endpoint='update_account_details')
@jwt_required()
@valid_session_required
@standard_session_required
def update_update_details():
    user_id = get_jwt_identity()
    updates = request.get_json()
    return update_account_helper(user_id, updates)


@patient_bp.route('ops/account/get-transactions', methods=['GET'], endpoint='get_transactions')
@jwt_required()
@valid_session_required
@standard_session_required
def get_transactions():
    user_id = get_jwt_identity()
    return get_transactions_helper(user_id)


@patient_bp.route('ops/account/make-transaction', methods=['POST'], endpoint='make_transaction')
@jwt_required()
@valid_session_required
@standard_session_required
def make_transactions():
    user_id = get_jwt_identity()
    details = request.get_json()
    return make_transaction_helper(user_id, details)


@patient_bp.route('ops/account/get-appointments', methods=['GET'], endpoint='get_appointments')
@jwt_required()
@valid_session_required
@standard_session_required
def get_appointments():
    user_id = get_jwt_identity()
    return get_appointments_helper(user_id)


@patient_bp.route('ops/account/book-appointment', methods=['GET'], endpoint='book_appointments')
@jwt_required()
@valid_session_required
@standard_session_required
def book_appointments():
    user_id = get_jwt_identity()
    details = request.get_json()
    return book_appointment_helper(user_id, details)
