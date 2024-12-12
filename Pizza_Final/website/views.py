from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from . import db, func
from .models import Pizza, PizzaPrice, Topping, PizzaOrder, OrderHistory

views = Blueprint('views', __name__)




@views.route('/', methods=['GET', 'POST'])
def home():
    """
    This is the main page where you choose which pizza to order and what size. 
    The selected pizzas are added to the PizzaOrder table and when the order button is pressed the records in the OrderPizza table is copied into the OrderHistory table so that the employees can see which orders are coming in.
    """
    selected_pizza = None
    current_price = 0
    if request.method == 'POST':
        # info about which pizza was orderd is gathered form the 'submit_pizza' button
        submit = request.form.get('submit_pizza')
        if submit:
            pizza_id = submit.split('_')[1]
            pizza = Pizza.query.filter_by(id=pizza_id).first()
            pizza_name = pizza.name
            size = request.form.get(f"{pizza_id}_size")
            price = request.form.get(f"{pizza_id}_price_{size.lower()}")
            
            flash(f"You have selected {pizza_name} ({size}) for {price}kr!", 'success')
            
            new_order = PizzaOrder(name=pizza_name, size=size, price=price)
            db.session.add(new_order)
            db.session.commit()
            
            # gets the current total price for the pizza order
            current_price = db.session.query(func.sum(PizzaOrder.price)).scalar()
        
        makeOrder = request.form.get('makeOrder')
        if makeOrder == 'makeOrder':          
            
            orders = PizzaOrder.query.all()
            # max_order is the keeps track of how many orders there are. the code checks the current orderID and increments it by one
            max_order_id = db.session.query(func.max(OrderHistory.orderID)).scalar()
            new_order_id = max_order_id if max_order_id is not None else 0
            new_order_id = int(new_order_id)
            new_order_id += 1
            
            # gets teh total price again (might be unncessary) and copies over the PizzaOrder records to the OrderHistory table. An orderID field and date field is also added
            total_price = db.session.query(func.sum(PizzaOrder.price)).scalar()
            for order in orders:
                new_order = OrderHistory(orderID=new_order_id, name=order.name, size=order.size, price=order.price, totalPrice=total_price)
                db.session.add(new_order)
            db.session.commit()

            # The PizzaOrder table is emptied/deleted so that a new order can be made
            db.session.query(PizzaOrder).delete()
            db.session.commit()
            
            
            flash(f"Order Submitted! for {total_price}kr! Thank you for shopping at Exploding Pizza &#x1F600 ", 'success')
            return redirect(url_for('views.home'))
            
            
    pizzas = Pizza.query.all()
    prices = PizzaPrice.query.all()
    toppings = Topping.query.all()
    orders = PizzaOrder.query.all()
    return render_template('home.html', pizzas=pizzas, prices=prices, toppings=toppings, orders=orders, current_price=current_price, is_in_stock=is_in_stock)




@views.route('/remove_order/<int:order_id>', methods=['POST'])
def remove_order(order_id):
    """
    This function deletes a record from the PizzaOrder table. If the customer regrets adding a pizza they can remove it and make another choice
    """
    order = PizzaOrder.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f"Order {order_id} removed!", 'success')
    return redirect(url_for('views.home'))



def is_in_stock(toppingsList, toppings):
    """
    This function compares the records toppings that have been added to each pizza with stock/inventory status of that topping. If a topping value is 'nothing' that pizza cannot be ordered.
    """
    for pizzaTopping in toppingsList:
        x = str(pizzaTopping)[1:-1].strip()
        for topping in toppings:
            if repr(topping.name) == str(pizzaTopping)[1:-1]:
                if topping.inventory == 'nothing':
                    return 'nothing'
    return 'little'























