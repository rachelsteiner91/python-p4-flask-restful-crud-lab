#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST #
    def post(self):

        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)

# PATCH #
## make a PATCH request with an object in the body that updates one plant ## return the updated plant in the response
    def patch(self, id):
        data = request.get_json()
        plant = Plant.query.filter_by(id=id).first() 

        for attr in data:
            setattr(plant, attr, data[attr])
        
        db.session.add(plant)
        db.session.commit()

        return make_response(plant.to_dict(), 200)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 # DELETE #
 # the DELETE request should delete one plant from the data base
 # return an empty string aka '' with the status code 204 (no content)to indicate a successful deletion    
    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        db.session.delete(plant)
        db.session.commit()

        return make_response('', 204)

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
