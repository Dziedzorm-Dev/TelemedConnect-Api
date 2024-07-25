from flask import Blueprint, request
from core.controllers_helper import signup_helper, signin_helper

medical_officer_auth_bp = Blueprint('medical_officer_auth', __name__)


@medical_officer_auth_bp .route('/doctor/signup', methods=['POST'])
def signup_doctor():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    return signup_helper(email, password, 3)


@medical_officer_auth_bp .route('/doctor/signin', methods=['POST'])
def signin_doctor():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    is_30_days = data.get('30_days', False)
    return signin_helper(email, password, 3, is_30_days)


@medical_officer_auth_bp .route('/pharmacist/signup', methods=['POST'])
def signup_pharmacist():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    return signup_helper(email, password, 2)


@medical_officer_auth_bp .route('/pharmacist/signin', methods=['POST'])
def signin_pharmacist():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    is_30_days = data.get('30_days', False)
    return signin_helper(email, password, 2, is_30_days)


@medical_officer_auth_bp .route('/lab-technician/signup', methods=['POST'])
def signup_lab_technician():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    return signup_helper(email, password, 1)


@medical_officer_auth_bp.route('/lab-technician/signin', methods=['POST'])
def signin_lab_technician():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    is_30_days = data.get('30_days', False)
    return signin_helper(email, password, 1, is_30_days)

