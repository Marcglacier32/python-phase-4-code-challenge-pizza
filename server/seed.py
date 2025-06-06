#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    # Delete from the many-to-many table first (RestaurantPizza)
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    # Add restaurants
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='123 Karen Street')
    bistro = Restaurant(name="Sanjay's Pizza", address='456 Sanjay Avenue')
    palace = Restaurant(name="Kiki's Pizza", address='789 Kiki Boulevard')
    db.session.add_all([shack, bistro, palace])

    # Add pizzas
    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red Peppers, Mustard")
    db.session.add_all([cheese, pepperoni, california])

    # Add restaurant-pizza relationships
    print("Creating restaurant_pizzas...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=10)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=15)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=12)
    db.session.add_all([pr1, pr2, pr3])

    db.session.commit()
    print("🌱 Seeding complete!")
