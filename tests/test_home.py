from http import HTTPStatus


def test_home_api(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    # Response is binary string data because data is the raw data of the output.
    # The switch from ' to " is due to json serialization
    assert response.data == b'{"data":"OK"}\n'
    # json allows us to get back a deserialized data structure without us needing to manually do it
    assert response.json == {'data': 'OK'}


def test_dummy_model_api(client):
    response = client.post('/dummy_model', json={
        'value': 'foobar'
    })
    assert response.status_code == HTTPStatus.OK
    obj = response.json
    new_id = obj.get('id')
    response = client.get(f'/dummy_model/{new_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json.get('value') == 'foobar'


def test_get_appointments_in_window(client):
    response = client.get('/appointments/doctor/1?start_time=2020-01-01 09:00&end_time=2020-01-01 10:00')
    assert response.status_code == HTTPStatus.OK
    assert response.json == [{'doctor_id': 1, 'duration': 30, 'end_time': 'Wed, 01 Jan 2020 09:30:00 GMT', 'id': 1, 'start_time': 'Wed, 01 Jan 2020 09:00:00 GMT'}, {'doctor_id': 1, 'duration': 30, 'end_time': 'Wed, 01 Jan 2020 10:00:00 GMT', 'id': 2, 'start_time': 'Wed, 01 Jan 2020 09:30:00 GMT'}]


def test_get_appointments_in_window_no_appointments(client):
    response = client.get('/appointments/doctor/2?start_time=2020-01-01 15:00&end_time=2020-01-01 16:00')
    assert response.status_code == HTTPStatus.OK
    assert response.json == []


def test_get_appoints_date_failure(client):
    response = client.get('/appointments/doctor/2?start_time=asdf&end_time=asdf')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json.get('error') == 'Invalid date format for asdf. Please use %Y-%m-%d %H:%M'


def test_create_appointment(client):
    response = client.post('/appointments', json={
        'doctor_id': 1,
        'duration': 30,
        'start_time': '2019-01-01 11:00',
        'end_time': '2019-01-01 11:30'
    })
    assert response.status_code == HTTPStatus.OK
    obj = response.json
    new_id = obj.get('id')
    assert response.json.get('doctor_id') == 1
    assert response.json.get('duration') == 30
    assert response.json.get('start_time') == 'Tue, 01 Jan 2019 11:00:00 GMT'
    assert response.json.get('end_time') == 'Tue, 01 Jan 2019 11:30:00 GMT'
    assert response.json.get('id') == new_id


def test_create_appointment_outside_working_hours(client):
    response = client.post('/appointments', json={
        'doctor_id': 1,
        'duration': 30,
        'start_time': '2022-01-01 09:00',
        'end_time': '2022-01-01 09:30'
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json.get('error') == 'Doctor Strange is not available at the given time window'

def test_create_appointment_overlap(client):
    response = client.post('/appointments', json={
        'doctor_id': 1,
        'duration': 30,
        'start_time': '2020-01-01 09:30',
        'end_time': '2020-01-01 10:00'
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json.get('error') == 'Doctor Strange has an appointment at the given time window'

def test_create_first_available_appointment(client):
    response = client.post('/appointments/1/first_available', json={
        'duration': 30,
        'start_time': '2020-01-01 09:00',
    })
    assert response.status_code == HTTPStatus.OK
    obj = response.json
    new_id = obj.get('id')
    assert response.json.get('doctor_id') == 1
    assert response.json.get('duration') == 30
    assert response.json.get('start_time') == 'Wed, 01 Jan 2020 10:00:00 GMT'
    assert response.json.get('end_time') == 'Wed, 01 Jan 2020 10:30:00 GMT'
    assert response.json.get('id') == new_id


def test_create_first_available_appointment_late(client):
    response = client.post('/appointments/1/first_available', json={
        'duration': 60,
        'start_time': '2020-01-01 12:00',
    })
    assert response.status_code == HTTPStatus.OK
    obj = response.json
    new_id = obj.get('id')
    assert response.json.get('doctor_id') == 1
    assert response.json.get('duration') == 60
    assert response.json.get('start_time') == 'Wed, 01 Jan 2020 12:00:00 GMT'
    assert response.json.get('end_time') == 'Wed, 01 Jan 2020 13:00:00 GMT'
    assert response.json.get('id') == new_id


def test_create_first_available_appointment_early(client):
    response = client.post('/appointments/2/first_available', json={
        'duration': 15,
        'start_time': '2020-01-01 08:00',
    })
    assert response.status_code == HTTPStatus.OK
    obj = response.json
    new_id = obj.get('id')
    assert response.json.get('duration') == 15
    assert response.json.get('start_time') == 'Wed, 01 Jan 2020 08:00:00 GMT'
    assert response.json.get('end_time') == 'Wed, 01 Jan 2020 08:15:00 GMT'
    assert response.json.get('id') == new_id


def test_create_first_available_appointment_not_found(client):
    response = client.post('/appointments/1/first_available', json={
        'duration': 60,
        'start_time': '2020-01-01 08:00',
    })
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == "Appointment not found"