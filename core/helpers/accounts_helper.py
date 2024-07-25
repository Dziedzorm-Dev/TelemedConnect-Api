from dateutil import parser
from flask import jsonify
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError

from core.models.account import Account
from core.models.appointment import Appointment
from core.models.availability import Availability
from core.models.transaction import Transaction
from core.utils.utils_ import generate_id


def get_account_details_helper(user_id):
    account = Account.query.filter_by(user_id=user_id).first()

    if not account:
        jsonify(
            flag={'value': 0, 'message': "Account dues not exist."},
            account_details=None,
        ), 404

    return jsonify(
        flag={'value': 1, 'message': "Query Successful."},
        account_details=account.get_details(),
    ), 200


def update_account_helper(user_id, updates):
    account = Account.query.filter_by(user_id=user_id).first()

    if not account:
        return jsonify(
            flag={'value': 0, 'message': "Account does not exist."},
            account_details=None,
        ), 404

    if updates is None or len(updates) == 0:
        return jsonify(
            flag={'value': 1, 'message': "There is nothing to update."}
        ), 201

    result = account.update(updates)
    if result == 1:
        return jsonify(
            flag={'value': 0, 'message': "Invalid dob provided."}
        ), 200

    return jsonify(
        flag={'value': 1, 'message': "Account updated Successfully."}
    ), 200


def get_transactions_helper(user_id):
    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        if not account:
            return jsonify(
                flag={'value': 0, 'message': "Account does not exist."},
                account_details=None,
            ), 404

    transactions = Transaction.query.filter(
        or_(Transaction.sender_id == user_id, Transaction.receiver_id == user_id)
    ).all()

    return jsonify(
        flag={'value': 1, 'message': "Successful."},
        transactions=[trxn.to_dict() for trxn in transactions]
    ), 200


def make_transaction_helper(user_id, details):
    required = [
        "amount",
        "currency",
        "receiver_id",
        "payment_method",
        "account_number",
        "description",
        "fee",
        "exchange_rate",
        "original_amount",
        "original_currency",
    ]

    if details is None:
        return jsonify(
            flag={'value': 0, 'message': "Transaction details not provided"}
        ), 403

    transaction = Transaction(sender_id=user_id, reference_number=generate_id()[:10])
    for key in required:
        if key not in details or details[key] is None:
            return jsonify(
                flag={'value': 0, 'message': "{} not provided".format(key)}
            ), 403

        setattr(transaction, key, details[key])

    transaction.create()

    return jsonify(
        flag={'value': 1, 'message': "Transaction created successfully."}
    ), 200


def get_appointments_helper(user_id):
    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        if not account:
            return jsonify(
                flag={'value': 0, 'message': "Account does not exist."},
                account_details=None,
            ), 404

    appointments = Transaction.query.filter(
        or_(Appointment.organiser_id == user_id, Appointment.invitee_id == user_id)
    ).all()

    return jsonify(
        flag={'value': 1, 'message': "Successful."},
        appointments=[apmnt.to_dict() for apmnt in appointments]
    ), 200


def is_slot_available(availabilities, apmnt):
    for avail in availabilities:
        if avail.start_time <= apmnt.start_time <= avail.end_time and avail.start_time <= apmnt.end_time <= avail.end_time:
            return True
    return False or len(availabilities) == 0


def book_appointment_helper(user_id, details):
    attr = ["invitee_id", "mode", "location", "coordinates", "start_time", "end_time", "purpose"]
    required = ["invitee_id","mode", "start_time", "end_time", "purpose"]

    appointment = Appointment(organiser_id=user_id)

    for key in attr:
        if key in required and (key not in details or details[key] is None):
            return jsonify(
                flag={'value': 0, 'message': "{} not provided".format(key)}
            ), 403
        else:
            value = details[key]
            if "time" in key:
                try:
                    date_obj = parser.parse(value)
                    value = date_obj.date()
                except (ValueError, parser.ParserError):
                    return jsonify(
                        flag={'value': 0, 'message': "Invalid {} provided".format(key)}
                    ), 403

            setattr(appointment, key, value)

    try:
        organiser_avails = Availability.query.filter_by(user_id=appointment.organiser_id).all()
        invitee_avails = Availability.query.filter_by(user_id=appointment.invitee_id).all()

        if not (is_slot_available(organiser_avails, appointment) and is_slot_available(invitee_avails, appointment)):
            msg = "One of the participants is not available during the requested time."
            return jsonify(
                flag={'value': 0, 'message': msg}
            ), 500

        # Check for conflicting appointments
        conflicting_appointments = Appointment.query.filter(
            or_(
                and_(Appointment.organiser_id == appointment.organiser_id,
                     Appointment.start_time <= appointment.end_time,
                     Appointment.end_time >= appointment.start_time),
                and_(Appointment.invitee_id == appointment.invitee_id,
                     Appointment.start_time <= appointment.end_time,
                     Appointment.end_time >= appointment.start_time)
            )
        ).all()

        if conflicting_appointments:
            msg = 'Appointment booking failed. There is a conflicting appointment for one of the participants during the requested time'
            return jsonify(
                result_flag={'value': 1, 'message': msg}
            ), 500

        appointment.create()

        return jsonify(
            flag={'value': 1, 'message': 'Appointment booking successful'}
        ), 200

    except SQLAlchemyError as e:
        print(e)
        return jsonify(
            result_flag={'value': 0, 'message': 'Something went wrong'}
        ), 500


def create_availability_helper(user_id):
    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        if not account:
            return jsonify(
                flag={'value': 0, 'message': "Account does not exist."},
                account_details=None,
            ), 404

    appointments = Transaction.query.filter(
        or_(Appointment.organiser_id == user_id, Appointment.invitee_id == user_id)
    ).all()

    return jsonify(
        flag={'value': 1, 'message': "Successful."},
        appointments=[apmnt.to_dict() for apmnt in appointments]
    ), 200