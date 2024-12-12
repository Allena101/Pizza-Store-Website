from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from . import db
from .models import Pizza, PizzaPrice, Topping, PizzaTopping, PizzaOrder, OrderHistory

# This vies collects routes that are related to what the staff would need to have access to make administration changes related to pizzas (e.g. adding and removing pizzas/toppings)
stock = Blueprint("stock", __name__)


@stock.route("/deletePizza", methods=["GET", "POST"])
def deletePizza():

    if request.method == "POST":
        if "delete_pizza" in request.form:
            pizza_name = request.form["pizzaName"]
            pizza = Pizza.query.filter_by(name=pizza_name).first()

            # Could have used cascade but tried implementing it to late which caused issues , but i worked fine to manually delete the pizzaID first from PizzaPrice and PizzaTopping and then finally just delete the record from the Pizza table so
            pizza_prices_to_delete = PizzaPrice.query.filter_by(pizza=pizza_name).all()
            for pizza_price in pizza_prices_to_delete:
                db.session.delete(pizza_price)

            pizza_toppings_to_delete = PizzaTopping.query.filter_by(
                pizza_id=pizza.id
            ).all()
            for pizza_topping in pizza_toppings_to_delete:
                db.session.delete(pizza_topping)

            db.session.delete(pizza)
            db.session.commit()
            flash(f"You have deleted {pizza_name} from the store", "success")
            return redirect(url_for("stock.deletePizza"))

        elif "delete_topping" in request.form:
            # I made it so that you can only delete a pizza or a topping at a time.
            topping_name = request.form["toppingName"]
            topping = Topping.query.filter_by(name=topping_name).first()
            db.session.delete(topping)
            db.session.commit()
            flash(f"You have deleted {topping_name} from the store", "success")
            return redirect(url_for("stock.deletePizza"))

    toppings = Topping.query.all()
    pizzas = Pizza.query.all()
    toppingList = []
    pizzaList = []
    # These loops are for getting a list of Pizza names and Toppings that can then be populated by the drop down menus (select tag).
    for pizza in pizzas:
        pizzaList.append(pizza.name)
    for topping in toppings:
        toppingList.append(topping.name)

    return render_template(
        "deletePizza.html",
        toppings=toppings,
        pizzas=pizzas,
        pizzaList=pizzaList,
        toppingList=toppingList,
        no_sidebar=True,
    )


@stock.route("/addPizza", methods=["GET", "POST"])
def addPizza():
    selected_ingredients = []
    if request.method == "POST":
        pizza_name = request.form.get("pizzaName")
        if pizza_name:
            pizza_price = request.form.get("pizzaPrice")
            # checks if the user did not put in a number in the pizzaPrice field.
            # The flash is not used but i read that i might be in other browsers so i kept it in.
            try:
                pizza_price = int(pizza_price)
            except ValueError:
                flash("Price must be an integer", "danger")
                return redirect(url_for("stock.addPizza"))

            # All the ingredients are gathered from the from (i decided on maximum 5 per pizza)
            ingredient1 = request.form.get("ingredient1")
            selected_ingredients.append(ingredient1)

            ingredient2 = request.form.get("ingredient2")
            selected_ingredients.append(ingredient2)

            ingredient3 = request.form.get("ingredient3")
            selected_ingredients.append(ingredient3)

            ingredient4 = request.form.get("ingredient4")
            selected_ingredients.append(ingredient4)

            ingredient5 = request.form.get("ingredient5")
            selected_ingredients.append(ingredient5)

            print(
                f"""{pizza_name=} toppings: {ingredient1}, {ingredient2}, {ingredient3},
                  {ingredient4}, {ingredient5} Pizza price is: {pizza_price}"""
            )

            new_pizza = Pizza(name=pizza_name)
            db.session.add(new_pizza)
            db.session.commit()

            # This loop adds all the selected ingredients to the pizza (the PizzaTopping table).
            # If the user did not make any selection the default is 'None' which is selected out by the
            # if i == 'none' condition.
            for i in selected_ingredients:
                if i == "None":
                    continue
                pizzaTopping = PizzaTopping(pizza_id=new_pizza.id, name=i)
                db.session.add(pizzaTopping)
            db.session.commit()

            # The Pizza Prize model has a setter that alters the price based on if the size field
            pizza_price_small = PizzaPrice(
                pizza=new_pizza.name, size="Small", price=pizza_price
            )
            db.session.add(pizza_price_small)

            pizza_price_medium = PizzaPrice(
                pizza=new_pizza.name, size="Medium", price=pizza_price
            )
            db.session.add(pizza_price_medium)

            pizza_price_large = PizzaPrice(
                pizza=new_pizza.name, size="Large", price=pizza_price
            )
            db.session.add(pizza_price_large)

            db.session.commit()

            flash("New pizza was added successfully!", "success")
            return redirect(url_for("views.home"))

        newTopping = request.form.get("toppingName")
        if newTopping:
            # I decided to have add Pizza and add Topping in the same route
            topping = Topping(name=newTopping)

            db.session.add(topping)
            db.session.commit()

            flash("New topping was added successfully!", "success")
            return redirect(url_for("stock.addPizza"))

    toppings = Topping.query.all()
    # add 'None' to the list which becomes the default if the user does not select any topping for that drop down menu.
    toppingList = ["None"]
    for topping in toppings:
        toppingList.append(topping.name)
    return render_template(
        "addPizza.html", toppings=toppings, toppingList=toppingList, no_sidebar=True
    )


@stock.route("/stockTopping", methods=["GET", "POST"])
def stockTopping():
    if request.method == "POST":
        # the button name should be renamed to change_topping_stock
        submit = request.form.get("submit_pizza")
        if submit:
            topping_id = request.form.get("topping_id")
            inventory = request.form.get(f"{topping_id}_size")

            # changes the inventory field based on which radio button is active
            topping_to_update = Topping.query.get(int(topping_id))
            topping_to_update.inventory = inventory
            db.session.commit()
            flash(f"Topping inventory changed to {inventory}!", "success")

    toppings = Topping.query.all()
    return render_template("stockTopping.html", toppings=toppings, no_sidebar=True)


@stock.route("/orderHistory", methods=["GET", "POST"])
def orderHistoryg():

    # orders the records so that the newest orders are displayed first (so that the staff can easily see new orders coming in)
    orders = OrderHistory.query.order_by(OrderHistory.orderID.desc())
    return render_template("orderHistory.html", orders=orders, no_sidebar=True)
