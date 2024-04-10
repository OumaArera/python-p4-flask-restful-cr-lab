#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = [{"id": plant.id, "name": plant.name, "image": plant.image, "price": str(plant.price)} for plant in plants]
        return jsonify(plant_list)

    def post(self):
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        if not all([name, image, price]):
            return jsonify({"error": "Missing required fields."}), 400

        new_plant = Plant(name=name, image=image, price=price)
        db.session.add(new_plant)
        db.session.commit()

        return jsonify({"id": new_plant.id, "name": new_plant.name, "image": new_plant.image, "price": str(new_plant.price)}), 201

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return jsonify({"error": "Plant not found"}), 404
        return jsonify({"id": plant.id, "name": plant.name, "image": plant.image, "price": str(plant.price)})

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)


