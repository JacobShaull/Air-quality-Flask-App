from openaq import OpenAQ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


api = OpenAQ()

def get_results():
    '''returns tuples conataining date and time, and air quality'''
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    tuples = [(result['date']['utc'], result['values'])for result in body['results]']]
    return tuples

app = Flask(__name__) # Create flask app instance
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3' # Configure database uri for SQLAlchemy
DB = SQLAlchemy(app) # Assign SQLAlchemy to Flask app

@app.route('/')
def root():
    return str(Record.query.filter(Record.value >= 18).all())

class Record(DB.Model):
    '''Reassigning id, datetime and value attributes'''
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25), nullable=False)
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"<{self.datetime}, {self.value}>"

# @app.route('/risky')
# def risky():
#     records = Record.query.filter(Record.value >= 18).all()
#     results = [(record.datetime, record.values) for record in records]
#     for datetime, value in records:
#         risky_records = Record(datetime=datetime, value=value)
#         DB.session.add(risky_records)
#     DB.session.commit()
#     return str(records)

@app.route('/refresh')
def refresh():
    """Refreshes database."""
    DB.drop_all()
    DB.create_all()
    tupe=get_results()
    for index,tuples in enumerate(tupe):
        records = Record(id=index, datetime=str(tuples[0]), value=tuples[1])
        DB.session.add(records)

    DB.session.commit()
    return 'Data refreshed!'
