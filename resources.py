from flask import request, make_response
from flask_restful import Resource
from models import db, Restaurant, Pizza, RestaurantPizza

class RestaurantsResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict(only=('id', 'name', 'address')) for r in restaurants], 200

class RestaurantByIDResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return restaurant.to_dict(), 200
        return {"error": "Restaurant not found"}, 404

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204

class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict(only=('id', 'name', 'ingredients')) for p in pizzas], 200

class RestaurantPizzasResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            price = int(data.get("price"))
            if price < 1 or price > 30:
                raise ValueError("Price must be between 1 and 30.")
            pizza_id = int(data.get("pizza_id"))
            restaurant_id = int(data.get("restaurant_id"))
        except (TypeError, ValueError):
            return {"errors": ["validation errors"]}, 400

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            return {"errors": ["Invalid pizza_id or restaurant_id"]}, 400

        rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(rp)
        db.session.commit()

        return rp.to_dict(), 201
