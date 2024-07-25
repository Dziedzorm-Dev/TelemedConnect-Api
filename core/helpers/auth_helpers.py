from flask import jsonify
from core.models.account import Account
from core.models.otp import OTP
from core.models.session_token import SessionToken


def sign_up_helper(email, password, role):
    if not email or not password:
        return jsonify(
            flag={'value': 0, 'message': 'Email, password and role are required'},
            access_token=None,
            otp_token=None
        ), 400

    account = Account.query.filter_by(email=email).first()
    if account:
        return jsonify(
            flag={'value': 0, 'message': "An account with the same email already exists. Log in if you're the one"},
            access_token=None,
            otp_token=None
        ), 401

    account = Account(email=email, password=password, role=role)
    account.create()

    access_token = SessionToken.create_token(account.user_id, role, 'sign up verification', 30)

    return jsonify(
        flag={'value': 1, 'message': 'Sign up successfully, proceed to verify your email'},
        access_token=access_token,
        otp_token=OTP.generate_otp(account)
    ), 200


def sign_in_helper(email, password, role):

    if not email or not password:
        return jsonify(
            flag={'value': 0, 'message': 'Email and password are required'},
            access_token=None,
            otp_token=None
        ), 400

    account = Account.sign_in(email, password, role)
    if account[1] == 401:
        return jsonify(
            flag={'value': 0, 'message': 'Account does not exist or invalid email or password'},
            access_token=None,
            otp_token=None
        ), 401

    elif account[1] == 404:
        return jsonify(
            flag={'value': 0, 'message': 'Account not found'},
            access_token=None
        ), 404

    access_token = SessionToken.create_token(account[0].user_id, role, 'sign in verification', 30)

    return jsonify(
        flag={'value': 1, 'message': 'Sign in successfully, proceed to otp verification'},
        access_token=access_token,
        otp_token=OTP.generate_otp(account[0])
    ), 200


def verify_otp_helper(user_id, otp_token, otp_code, use, role):

    if use is None or role is None:
        return jsonify(
            flag={'value': 0, 'message': 'Missing role or use'},
        ), 404

    if not otp_code:
        return jsonify(
            flag={'value': 0, 'message': 'OTP code is required'}
        ), 400

    if not otp_token:
        return jsonify(
            flag={'value': 0, 'message': 'OTP token is required'}
        ), 400

    otp_entry = OTP.query.filter_by(user_id=user_id, otp_token=otp_token, otp_code=otp_code).first()

    if not otp_entry:
        return jsonify(
            flag={'value': 0, 'message': 'Invalid OTP code'}
        ), 400

    print("here")

    if otp_entry.is_expired():
        return jsonify(
            flag={'value': 0, 'message': 'OTP is expired, request for a new OTP'}
        ), 400

    access_token = ''
    if use == "sign up verification" or use == "sign in verification":
        account = Account.query.filter_by(user_id=otp_entry.user_id).first()
        account.status = 1
        account.update()

        access_token = SessionToken.create_token(
            user_id=account.user_id,
            role=role,
            use=use,
            exp_time=5
        )

    otp_entry.delete()

    return jsonify(
        result_flag={'value': 1, 'message': 'OTP verified successfully'},
        access_token=access_token
    ), 200


def resend_otp_helper(user_id, email, otp_token):
    if not otp_token or not email:
        return jsonify(
            flag={'value': 0, 'message': 'OTP token and email are required'}
        ), 400

    account = Account.query.filter_by(user_id=user_id, email=email).first()
    if not account:
        return jsonify(
            flag={'value': 0, 'message': 'User does not exist'}
        ), 400

    otp_entry = OTP.query.filter_by(user_id=user_id, otp_token=otp_token).first()
    if not otp_entry:
        otp_token = OTP.generate_otp(account)
        return jsonify(
            flag={'value': 1, 'message': 'New OTP sent'},
            otp_token=otp_token
        ), 201

    if otp_entry.is_expired():
        otp_entry.delete()
        otp_token = OTP.generate_otp(account)
        return jsonify(
            flag={'value': 1, 'message': 'New OTP sent'},
            otp_token=otp_token
        ), 201

    OTP.resend_otp(otp_entry.otp_code, account.email)

    return jsonify(
        flag={'value': 1, 'message': 'OTP resent successfully'},
        otp_token=otp_entry.otp_token
    ), 200


def refresh_session_helper(user_id, exp_time, use, role):
    if use is None or role is None:
        return jsonify(
            result_flag={'value': 0, 'message': 'Missing role or use'},
        ), 404

    if use == "sign up verification" or use == "sign in verification":
        access_token = SessionToken.create_token(user_id, role, "standard use", exp_time)
        return jsonify(
            flag={'value': 1, 'message': 'Session refreshed successfully'},
            access_token=access_token
        ), 400

    return jsonify(
            flag={'value': 0, 'message': 'You do not have permission to refresh this session'}
        ), 201
