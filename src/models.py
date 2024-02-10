from datetime import timedelta
from src.extensions import db
from flask import jsonify
from datetime import datetime

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

    def has_availability(self, start_time, end_time) -> bool:
        """
        Checks if the doctor has availability for the given time window
        """
        for working_hour in self.working_hours:
            if working_hour.day_of_week == start_time.weekday() and working_hour.start_time >= start_time.time() and working_hour.end_time <= end_time.time():
                return True
        return False
    
    def has_appointment_overlap(self, start_time, end_time) -> bool:
        """
        Checks if the doctor has an appointment at the given time window
        """
        for appointment in self.appointments:
            if appointment.start_time >= start_time or appointment.end_time <= end_time:
                return True
        return False
    
    def first_appointment(self, start_time, duration) -> str:
        """
        Returns the first available appointment for the given time window
        """
        sorted_working_hours = self.working_hours.order_by(WorkingHours.day_of_week.asc())
        current_day = start_time.weekday()
        end_time = start_time + timedelta(minutes=duration)
        filtered_working_hours = list(filter(lambda x: x.day_of_week >= current_day, sorted_working_hours))

        for working_hour in filtered_working_hours:
            if working_hour.start_time <= start_time.time() and working_hour.end_time >= end_time.time():
                # We have found a working hour that fits the time window
                # Now we need to check if there are any appointments that overlap with this time window
                # If same day, then use current start and end times
                if working_hour.start_time.weekday() == current_day:
                    target_start_time = start_time
                    target_end_time = end_time
                else:
                    # If not same day, then use the start time of the working hour
                    target_start_time = working_hour.start_time
                    target_end_time = target_start_time + timedelta(minutes=duration)

                # Get appointments for the same day
                appointments = self.appointments.filter(Appointment.start_time.weekday() == target_start_time.weekday()).order_by(Appointment.start_time.asc())
                for appointment in appointments:
                    if (
                        (target_start_time >= appointment.start_time and target_end_time <= appointment.end_time) # In between
                        or (target_start_time <= appointment.start_time and target_end_time >= appointment.start_time) # Overlapping start
                        or (target_start_time <= appointment.end_time and target_end_time >= appointment.end_time) # Overlapping end
                    ):
                        # There is an appointment that overlaps with the target time window, move time window
                        target_start_time = appointment.end_time
                        target_end_time = target_start_time + timedelta(minutes=duration)
                
                if target_end_time <= working_hour.end_time:
                    # Check within working hours
                    appointment = Appointment(doctor_id=self.id, duration=duration, start_time=target_start_time, end_time=target_end_time)
                    return appointment
        return None


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