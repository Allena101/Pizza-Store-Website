from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime


# from . import db
from . import db
from .models import Pizza, PizzaPrice, Topping, PizzaTopping

stock = Blueprint('stock', __name__)




@stock.route('/deletePizza', methods=['GET', 'POST'])
def deletePizza():
    
    if request.method == 'POST':
        if 'delete_pizza' in request.form:
            pizza_name = request.form['pizzaName']
            pizza = Pizza.query.filter_by(name=pizza_name).first()
            
            pizza_prices_to_delete = PizzaPrice.query.filter_by(pizza=pizza_name).all()
            for pizza_price in pizza_prices_to_delete:
                db.session.delete(pizza_price)
                
            pizza_toppings_to_delete = PizzaTopping.query.filter_by(pizza_id=pizza.id).all()
            for pizza_topping in pizza_toppings_to_delete:
                db.session.delete(pizza_topping)    
            
            db.session.delete(pizza)
            db.session.commit()
            flash(f"You have deleted {pizza_name} from the store", 'success')
            
            
            
            
            return redirect(url_for('stock.deletePizza'))
        elif 'delete_topping' in request.form:
            topping_name = request.form['toppingName']
            topping = Topping.query.filter_by(name=topping_name).first()
            db.session.delete(topping)
            db.session.commit()
            flash(f"You have deleted {topping_name} from the store", 'success')
            return redirect(url_for('stock.deletePizza'))
            
    toppings = Topping.query.all()
    pizzas = Pizza.query.all()
    toppingList = []
    pizzaList = []
    for pizza in pizzas:
        pizzaList.append(pizza.name)
    for topping in toppings:
        toppingList.append(topping.name)
    return render_template('deletePizza.html', toppings=toppings, pizzas=pizzas, pizzaList=pizzaList, toppingList=toppingList, no_sidebar=True)
