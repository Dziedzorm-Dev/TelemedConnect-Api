from flask import Blueprint, request, jsonify
from core.models_models import db, MedicalRecord, MedicationPrescription, TreatmentPlan, TestAndScan
from core.models_helper import update_medical_records_helper, update_dispense_medication_prescription_helper
from core.models_helper import update_treatment_plan_helper, update_test_scan
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.controllers_wrappers import verified_account_required, active_session_required, doctor_required, \
    complete_account_required
from core.controllers_wrappers import pharmacist_required, lab_technician_required

medical_officer_bp = Blueprint('medical_officer', __name__)


@medical_officer_bp.route('/create-medical-record', methods=['POST'], endpoint='create_medical_record')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def create_medical_record():
    data = request.json
    doctor_id = get_jwt_identity()
    patient_id = data['patient_id']

    new_medical_record = MedicalRecord(patient_id=patient_id, doctor_id=doctor_id)

    db.session.add(new_medical_record)
    db.session.commit()

    return jsonify(result_flag={'value': 1, 'message': 'Medical record created successfully'}), 200


@medical_officer_bp.route('/update-medical-record', methods=['POST'], endpoint='update_medical_record')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def update_medical_record():
    data = request.json()
    doctor_id = get_jwt_identity()
    medical_record_id = data['medical_record_id']
    _id = data.get('id')

    record = MedicalRecord.query.filter_by(id=_id).first()
    update_medical_records_helper(record, data)

    return jsonify(result_flag={'value': 1, 'message': 'Medical record updated successfully'}), 200


@medical_officer_bp.route('/create-test-scan', methods=['POST'], endpoint='creat_test_scan')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def create_test_scan():
    data = request.json()
    medical_record_id = data['medical_record_id']

    new_test_scan = TestAndScan(medical_record_id=medical_record_id)

    db.session.add(new_test_scan)
    db.session.commit()

    return jsonify(result_flag={'value': 1, 'message': 'TestScan created successfully'}), 200


@medical_officer_bp.route('/update-test-scan', methods=['POST'], endpoint='update_test_scan')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def update_test_scan():
    data = request.json()
    doctor_id = get_jwt_identity()
    patient_id = data['patient_id']
    medical_record_id = data['medical_record_id']
    _id = data['id']

    test_scan = TestAndScan.query.filter_by(id=_id).first()

    update_test_scan(test_scan, data)

    return jsonify(result_flag={'value': 1, 'message': 'TestScan updated successfully'}), 200


@medical_officer_bp.route('/record-test-scan-result', methods=['POST'], endpoint='record_test_scan_result')
@jwt_required
@verified_account_required
@active_session_required
@lab_technician_required
@complete_account_required
def record_test_scan_result():
    data = request.json()
    technician_id = get_jwt_identity()
    _id = data['id']
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')
    medical_record_id = data.get('medical_record_id')

    test_scan = TestAndScan.query.filter_by(id=_id).first()

    test_scan.technician_id = technician_id
    update_test_scan(test_scan, data)

    return jsonify(result_flag={'value': 1, 'message': 'TestScan result recorded successfully'}), 200


@medical_officer_bp.route('/create-treatment-plan', methods=['POST'], endpoint='create_treatment_plan')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def create_treatment_plan():
    data = request.json()
    doctor_id = get_jwt_identity()
    patient_id = data['patient_id']
    medical_record_id = data['medical_record_id']

    new_plan = TreatmentPlan(medical_record_id=medical_record_id)

    db.session.add(new_plan)
    db.session.commit()

    return jsonify(result_flag={'value': 1, 'message': 'Treatment updated successfully'}), 200


@medical_officer_bp.route('/update-treatment-plan', methods=['POST'], endpoint='update_treatment_plan')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def update_treatment_plan():
    data = request.json()
    _id = data['id']
    doctor_id = get_jwt_identity()
    patient_id = data['patient_id']
    medical_record_id = data['medical_record_id']

    plan = TreatmentPlan.query.filter_by(id=_id).first()

    update_treatment_plan_helper(plan, data)

    return jsonify(result_flag={'value': 1, 'message': 'Medical record updated successfully'}), 200


@medical_officer_bp.route('/create-medication-prescription', methods=['POST'], endpoint='create_medication_prescription')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def create_medication_prescription():
    data = request.json()
    doctor_id = get_jwt_identity()
    patient_id = data['medical_record_id']
    treatment_plan_id = data['treatment_plan_id']

    new_prescription = MedicationPrescription(treatment_plan_id=treatment_plan_id)

    db.session.add(new_prescription)
    db.session.commit()

    return jsonify(result_flag={'value': 1, 'message': 'Prescription created successfully'}), 200


@medical_officer_bp.route('/update-medication-prescription', methods=['POST'], endpoint='update_medication_prescription')
@jwt_required
@verified_account_required
@active_session_required
@doctor_required
@complete_account_required
def update_medication_prescription():
    data = request.json()
    _id = data['id']
    medical_officer_id = get_jwt_identity()

    prescription = MedicationPrescription.query.filter_by(id=_id,).first()

    update_medical_records_helper(prescription, data)

    return jsonify(result_flag={'value': 1, 'message': 'Medical record updated successfully'}), 200


@medical_officer_bp.route('/dispense-medication-prescription', methods=['POST'], endpoint='dispense_medication_prescription')
@jwt_required
@verified_account_required
@active_session_required
@pharmacist_required
@complete_account_required
def dispense_medication_prescription():
    data = request.json()
    dispensing_officer_id = get_jwt_identity()
    _id = data['id']
    patient_id = data['patient_id']
    doctor_id = data['doctor_id']

    prescription = MedicationPrescription.query.filter_by(id=_id).first()

    prescription.dispensing_officer_id = dispensing_officer_id

    update_dispense_medication_prescription_helper(prescription, data)

    return jsonify(result_flag={'value': 1, 'message': 'Prescription dispensed successfully'}), 200

