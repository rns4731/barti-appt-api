## Requirements

The requirements are as follows:

- Implement a model to represent an appointment with one of two doctors (Strange, Who). Appointments can be arbitrary length i.e. 20 mins, 45 mins, 60 mins
- Implement a model to represent the working hours of each doctor (9 AM to 5 PM, M-F for Strange, 8 AM to 4 PM M-F for Who). You can assume working hours are the same every week. i.e. The schedule is the same each week.
- Implement an API to create an appointment, rejecting it if there's a conflict.
- Implement an API to get all appointments within a time window for a specified doctor.
- Implement an API to get the first available appointment after a specified time. i.e. I'm a patient and I'm looking for the first available appointment

## Setup
1. After cloning this repository, cd into it.
2. Set up virtual environment via ```python3 -m venv env``` 
3. Activate the virtual environment via ```source env/bin/activate```
4. If it's properly set up, ```which python``` should point to a python under api-skeleton/env.
5. Install dependencies via ```pip install -r requirements.txt```

## Starting local flask server
Under api-skeleton/src, run ```flask run --host=0.0.0.0 -p 8000```

By default, Flask runs with port 5000, but some MacOS services now listen on that port.

## Running unit tests
All the tests can be run via ```pytest``` under api-skeleton directory.

## Code Structure
This is meant to be barebones.

* src/app.py contains the code for setting up the flask app.
* src/endpoints.py contains all the code for enpoints.
* src/models.py contains all the database model definitions.
* src/extensions.py sets up the extensions (https://flask.palletsprojects.com/en/2.0.x/extensions/)
