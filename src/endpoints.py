from flask import Blueprint, jsonify
from http import HTTPStatus
from src.extensions import db
from src.models import DummyModel, Doctor, WorkingHours, Appointment
from webargs import fields
from webargs.flaskparser import use_args

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
    print(args)
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
