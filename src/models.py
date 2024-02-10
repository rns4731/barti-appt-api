from src.extensions import db
from flask import jsonify


class DummyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to JSON
        """
        return jsonify({'id': self.id, 'value': self.value})

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to JSON
        """
        return jsonify({'id': self.id, 'name': self.name, 'email': self.email})


class WorkingHours(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    # Here 0 is Monday and 6 is Sunday
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def json(self) -> str:
        """ 
        :return: Serializes this object to JSON
        """
        return jsonify({'id': self.id, 'doctor_id': self.doctor_id, 'day': self.day, 'start_time': self.start_time, 'end_time': self.end_time})


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    # In minutes
    duration = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to JSON
        """
        return jsonify({'id': self.id, 'doctor_id': self.doctor_id, 'duration': self.duration, 'start_time': self.start_time, 'end_time': self.end_time})