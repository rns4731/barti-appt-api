from src.extensions import db
from flask import jsonify


class DummyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to a JSON response
        """
        return jsonify({'id': self.id, 'value': self.value})

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    working_hours = db.relationship('WorkingHours', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def json(self) -> str:
        """
        :return: Serializes this object to a JSON response
        """
        working_hours = [working_hour.json().json for working_hour in self.working_hours]
        appointments = [appointment.json().json for appointment in self.appointments]
        return jsonify({'id': self.id, 'name': self.name, 'email': self.email, 'working_hours': working_hours, 'appointments': appointments})


class WorkingHours(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    # Here 0 is Monday and 6 is Sunday
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def json(self) -> str:
        """ 
        :return: Serializes this object to a JSON response
        """
        return jsonify({'id': self.id, 'doctor_id': self.doctor_id, 'day': self.day_of_week, 'start_time': self.start_time.strftime("%H:%M"), 'end_time': self.end_time.strftime("%H:%M")})


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    # In minutes
    duration = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to a JSON response
        """
        return jsonify({'id': self.id, 'doctor_id': self.doctor_id, 'duration': self.duration, 'start_time': self.start_time, 'end_time': self.end_time})