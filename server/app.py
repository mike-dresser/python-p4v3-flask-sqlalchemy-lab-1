# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakes_by_id(id):
    q = Earthquake.query.filter_by(id=id).first()
    if q:
        body = q.to_dict()
        response = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        response = 404
    return make_response(body, response)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    q = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    result = []
    for quake in q:
        result.append(quake.to_dict())
    response = {'count': len(result), 
                'quakes': result
                }
    return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
