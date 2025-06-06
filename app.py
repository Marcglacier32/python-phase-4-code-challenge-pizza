#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

from resources import (
    RestaurantsResource,
    RestaurantByIDResource,
    PizzasResource,
    RestaurantPizzasResource
)

api.add_resource(RestaurantsResource, "/restaurants")
api.add_resource(RestaurantByIDResource, "/restaurants/<int:id>")
api.add_resource(PizzasResource, "/pizzas")
api.add_resource(RestaurantPizzasResource, "/restaurant_pizzas")


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {"error": "Restaurant not found"}, 404

    # Serialize restaurant including related restaurant_pizzas and pizzas
    restaurant_dict = restaurant.to_dict()
    
    # Add restaurant_pizzas with nested pizza data
    restaurant_pizzas = []
    for rp in restaurant.restaurant_pizzas:
        rp_dict = rp.to_dict()
        rp_dict["pizza"] = rp.pizza.to_dict()
        restaurant_pizzas.append(rp_dict)
    
    restaurant_dict["restaurant_pizzas"] = restaurant_pizzas

    return restaurant_dict, 200

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {"error": "Restaurant not found"}, 404

    db.session.delete(restaurant)
    db.session.commit()
    return "", 204

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")

    errors = []

    # Validate price
    if not isinstance(price, (int, float)) or price < 1 or price > 30:
        errors.append("Price must be between 1 and 30.")

    # Validate pizza and restaurant existence
    pizza = Pizza.query.get(pizza_id)
    if not pizza:
        errors.append("Pizza not found.")
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        errors.append("Restaurant not found.")

    if errors:
        return {"errors": errors}, 400

    new_rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)

    db.session.add(new_rp)
    db.session.commit()

    rp_dict = new_rp.to_dict()
    rp_dict["pizza"] = pizza.to_dict()
    rp_dict["restaurant"] = restaurant.to_dict()

    return rp_dict, 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
