from flask import Blueprint, jsonify
from http import HTTPStatus
from src.extensions import db
from src.models import DummyModel, Doctor, WorkingHours, Appointment
from webargs import fields
from webargs.flaskparser import use_args
from datetime import datetime

home = Blueprint('/', __name__)


# Helpful documentation:
# https://webargs.readthedocs.io/en/latest/framework_support.html
# https://flask.palletsprojects.com/en/2.0.x/quickstart/#variable-rules

@home.route('/')
def index():
    return {'data': 'OK'}


@home.route('/dummy_model/<id_>', methods=['GET'])
def dummy_model(id_):
    record = DummyModel.query.filter_by(id=id_).first()
    if record is not None:
        return record.json()
    else:
        return jsonify(None), HTTPStatus.NOT_FOUND


@home.route('/dummy_model', methods=['POST'])
@use_args({'value': fields.String()})
def dummy_model_create(args):
    new_record = DummyModel(value=args.get('value'))
    db.session.add(new_record)
    db.session.commit()
    return new_record.json()


@home.route('/doctors/<id_>', methods=['GET'])
def doctor(id_):
    record = Doctor.query.filter_by(id=id_).first()
    if record is not None:
        return record.json()
    else:
        return jsonify(None), HTTPStatus.NOT_FOUND


@home.route('/doctors', methods=['GET'])
def doctors():
    records = Doctor.query.all()
    response = [record.json().json for record in records]
    return response


@home.route('/appointments', methods=['GET'])
def appointments():
    records = Appointment.query.all()
    return jsonify([record.json().json for record in records])


@home.route('/appointments', methods=['POST'])
@use_args({
    'doctor_id': fields.Integer(required=True),
    'duration': fields.Integer(required=True),
    'start_time': fields.String(required=True),
    'end_time': fields.String(required=True)
}, location='json')
def appointments_create(args):
    format = "%Y-%m-%d %H:%M"
    start_time = args.get('start_time')
    end_time = args.get('end_time')
    for t in [start_time, end_time]:
        try:
            datetime.strptime(t, format)
        except ValueError:
            return jsonify({'error': f"Invalid date format for {t}. Please use {format}"}), HTTPStatus.BAD_REQUEST
    start_time = datetime.strptime(start_time, format)
    end_time = datetime.strptime(end_time, format)
    doctor = Doctor.query.filter_by(id=args.get('doctor_id')).first()
    if not doctor.has_availability(start_time, end_time):
        return jsonify({'error': f"Doctor {doctor.name} is not available at the given time window"}), HTTPStatus.BAD_REQUEST
    if doctor.has_appointment_overlap(start_time, end_time):
        return jsonify({'error': f"Doctor {doctor.name} has an appointment at the given time window"}), HTTPStatus.BAD_REQUEST
    new_record = Appointment(doctor_id=args.get('doctor_id'), duration=args.get('duration'), start_time=start_time, end_time=end_time)
    db.session.add(new_record)
    db.session.commit()
    return new_record.json()


@home.route("/appointments/<id_>/first_available", methods=['POST'])
@use_args({
    'start_time': fields.String(required=True),
    "duration": fields.Integer(required=True)
}, location='json')
def first_available_appointment(args, id_):
    format = "%Y-%m-%d %H:%M"
    start_time = args.get('start_time')
    duration = args.get('duration')
    for t in [start_time]:
        try:
            datetime.strptime(t, format)
        except ValueError:
            return jsonify({'error': f"Invalid date format for {t}. Please use {format}"}), HTTPStatus.BAD_REQUEST
    start_time = datetime.strptime(start_time, format)     
    doctor = Doctor.query.filter_by(id=id_).first()
    appointment = doctor.first_appointment(start_time, duration)
    if appointment is not None:
        return appointment.json()
    else:
        return jsonify("Appointment not found"), HTTPStatus.NOT_FOUND


@home.route('/appointments/doctor/<id_>', methods=['GET'])
@use_args({
    'start_time': fields.String(required=True),
    "end_time": fields.String(required=True)
}, location='query')
def appointments_by_doctor_window(args, id_):
    format = "%Y-%m-%d %H:%M"
    start_time = args.get('start_time')
    end_time = args.get('end_time')
    for t in [start_time, end_time]:
        try:
            datetime.strptime(t, format)
        except ValueError:
            return jsonify({'error': f"Invalid date format for {t}. Please use {format}"}), HTTPStatus.BAD_REQUEST
    start_time = datetime.strptime(start_time, format)
    end_time = datetime.strptime(end_time, format)        
    records = Appointment.query.filter_by(doctor_id=id_).filter(Appointment.start_time >= start_time).filter(Appointment.end_time <= end_time).all()
    return jsonify([record.json().json for record in records])