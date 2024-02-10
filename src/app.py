from flask import Flask
from src.extensions import db
from src.endpoints import home
from src.models import Doctor, DummyModel, WorkingHours, Appointment
from datetime import datetime


def seed_data():
    """
    Helper function to seed data into the database to keep things simple.
    This should ideally run as a custom script via the flask cli.
    """
    record = DummyModel(value='Hello World')
    db.session.add(record)

    doctor1 = Doctor(name='Strange', email="doc1@gmail.com")
    doctor2 = Doctor(name='Who', email="doc2@gmail.com")
    db.session.add(doctor1)
    db.session.add(doctor2)

    db.session.commit()

    start_time_1 = datetime.strptime("09:00", "%H:%M")
    end_time_1 = datetime.strptime("17:00", "%H:%M")

    start_time_2 = datetime.strptime("08:00", "%H:%M")
    end_time_2 = datetime.strptime("16:00", "%H:%M")

    for i in range(0, 5):
        working_hours_doc_1 = WorkingHours(doctor_id=doctor1.id, day_of_week=i, start_time=start_time_1.time(), end_time=end_time_1.time())
        db.session.add(working_hours_doc_1)
    
    for i in range(0, 5):
        working_hours_doc_2 = WorkingHours(doctor_id=doctor2.id, day_of_week=i, start_time=start_time_2.time(), end_time=end_time_2.time())
        db.session.add(working_hours_doc_2)

    db.session.commit()

    appointment_1 = Appointment(doctor_id=doctor1.id, duration=30, start_time=datetime.strptime("2020-01-01 09:00", "%Y-%m-%d %H:%M"), end_time=datetime.strptime("2020-01-01 09:30", "%Y-%m-%d %H:%M"))
    appointment_2 = Appointment(doctor_id=doctor1.id, duration=30, start_time=datetime.strptime("2020-01-01 09:30", "%Y-%m-%d %H:%M"), end_time=datetime.strptime("2020-01-01 10:00", "%Y-%m-%d %H:%M"))
    appointment_3 = Appointment(doctor_id=doctor2.id, duration=30, start_time=datetime.strptime("2020-01-01 10:00", "%Y-%m-%d %H:%M"), end_time=datetime.strptime("2020-01-01 10:30", "%Y-%m-%d %H:%M"))
    appointment_4 = Appointment(doctor_id=doctor2.id, duration=30, start_time=datetime.strptime("2020-01-01 10:30", "%Y-%m-%d %H:%M"), end_time=datetime.strptime("2020-01-01 11:00", "%Y-%m-%d %H:%M"))
    appointment_5 = Appointment(doctor_id=doctor2.id, duration=60, start_time=datetime.strptime("2020-01-01 11:00", "%Y-%m-%d %H:%M"), end_time=datetime.strptime("2020-01-01 12:00", "%Y-%m-%d %H:%M"))
    db.session.add(appointment_1)
    db.session.add(appointment_2)
    db.session.add(appointment_3)
    db.session.add(appointment_4)
    db.session.add(appointment_5)

    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    # We are doing a create all here to set up all the tables. Because we are using an in memory sqllite db, each
    # restart wipes the db clean, but does have the advantage of not having to worry about schema migrations.
    with app.app_context():
        db.create_all()
        seed_data()
    app.register_blueprint(home)
    return app
