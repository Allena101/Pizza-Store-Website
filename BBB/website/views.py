from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
# from .models import Note
# from models import db
# from website.models import db
import json
from datetime import datetime


# from . import db
from . import db
from .models import User, Pizza, PizzaPrice, Topping, PizzaTopping, PizzaOrder, OrderHistory

views = Blueprint('views', __name__)



# @views.route('/', methods=['GET', 'POST'])
# def home():
#     pizzas = Pizza.query.all()
#     toppings = Topping.query.all()
#     pizzaToppings = PizzaTopping.query.all()
#     selected_pizza = None
#     if request.method == 'POST':
#         # Retrieve selected pizza name and size
#         pizza_name = request.form.get('pizzaName')
#         size = request.form.get('size')
#         selected_pizza = f"{pizza_name} - {size}"
#     return render_template('home.html', pizzas=pizzas, selected_pizza=selected_pizza)




def is_in_stock(toppingsList, toppings):
    for pizzaTopping in toppingsList:
        # print(pizzaTopping)
        x = str(pizzaTopping)[1:-1].strip()
        # print(x)
        for topping in toppings:
            # print(topping.name)
            # print(str(topping.name))
            # print(repr(topping.name))
            if repr(topping.name) == str(pizzaTopping)[1:-1]:
                # print(' XXXXXXXXXXXXXXXX ')
                # print(pizzaTopping, topping.name)
                if topping.inventory == 'nothing':
                    return 'nothing'
    return 'little'

# def is_in_stock(toppingsList, toppings):
#     for pizzaTopping in toppingsList:
#         print(pizzaTopping)
#         # print(f'{pizzaTopping}')
#         # print(str(pizzaTopping)[1:-1]).strip()
#         x = str(pizzaTopping)[1:-1].strip()
#         print(x)
#         for topping in toppings:
#             print(topping.name)
#             print(str(topping.name))
#             print(repr(topping.name))
#             # y = repr(topping.name)
#             # print(y)
#             # if str(pizzaTopping)[1:-1] == topping.name:
#             if repr(topping.name) == str(pizzaTopping)[1:-1]:
#                 print(' XXXXXXXXXXXXXXXX ')
#                 # print(pizzaTopping, topping.name)
#                 if topping.inventory == 'nothing':
#                     return False
#     return True



@views.route('/', methods=['GET', 'POST'])
def home():
    selected_pizza = None
    if request.method == 'POST':
        # submit = request.form.get('submit')
        submit = request.form.get('submit_pizza')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        if submit:
            pizza_id = submit.split('_')[1]
            pizza = Pizza.query.filter_by(id=pizza_id).first()
            pizza_name = pizza.name
            size = request.form.get(f"{pizza_id}_size")
            price = request.form.get(f"{pizza_id}_price_{size.lower()}")         
                     
            selected_pizza = f"You have selected {pizza_name} ({size}) {price}"                 
            
            flash(f"You have selected {pizza_name} ({size}) for {price}kr!", 'success')
            
            new_order = PizzaOrder(name=pizza_name, size=size, price=price)
            db.session.add(new_order)
            db.session.commit()
        
        makeOrder = request.form.get('makeOrder')
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        if makeOrder == 'makeOrder':
            print('CCCCCCCCCCCCCCCCCCCCCCCC')
            orders = PizzaOrder.query.all()
            for order in orders:
                # print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
                # print(order)
                new_order = OrderHistory(name=order.name, size=order.size, price=order.price)
                db.session.add(new_order)
            db.session.commit()
            
    pizzas = Pizza.query.all()
    prices = PizzaPrice.query.all()
    toppings = Topping.query.all()
    orders = PizzaOrder.query.all()
    return render_template('home.html', pizzas=pizzas, selected_pizza=selected_pizza, prices=prices, toppings=toppings, orders=orders, is_in_stock=is_in_stock)



@views.route('/addPizza', methods=['GET', 'POST'])
def addPizza():
    selected_ingredients = []
    if request.method == 'POST':
        pizza_name = request.form.get('pizzaName')
        if pizza_name:
            pizza_price = request.form.get('pizzaPrice')
            
            ingredient1 = request.form.get('ingredient1')
            selected_ingredients.append(ingredient1)
            
            ingredient2 = request.form.get('ingredient2')
            selected_ingredients.append(ingredient2)
            
            ingredient3 = request.form.get('ingredient3')
            selected_ingredients.append(ingredient3)
            
            ingredient4 = request.form.get('ingredient4')        
            selected_ingredients.append(ingredient4)
            
            ingredient5 = request.form.get('ingredient5')   
            selected_ingredients.append(ingredient5)
                
            print(f"""{pizza_name=} toppings: {ingredient1}, {ingredient2}, {ingredient3},
                  {ingredient4}, {ingredient5} Pizza price is: {pizza_price}""")
            
            
            new_pizza = Pizza(name=pizza_name)
            db.session.add(new_pizza)
            db.session.commit()
            
            for i in selected_ingredients:
                pizzaTopping =  PizzaTopping(pizza_id=new_pizza.id, name=i)
                db.session.add(pizzaTopping)
            db.session.commit()
            
            # remoze size after you have updated models since medium will be default
            pizza_price = PizzaPrice(pizza=new_pizza.name, size='Medium', price=pizza_price)
            db.session.add(pizza_price)
            db.session.commit()
            
            # create the flash messege. if you can make it so that it can . make one for both pizza and topping
            

            # Create a new Pizza object
            # pizza = Pizza(name=pizza_name, ingredients=selected_ingredients)
            # # Add the new object to the database
            # db.session.add(pizza)
            # db.session.commit()

            flash('New pizza added successfully!', 'success')
            return redirect(url_for('views.home'))
        

        newTopping = request.form.get('toppingName')
        if newTopping:
            # Create a new Topping object
            topping = Topping(name=newTopping)

            # Add the new object to the database
            db.session.add(topping)
            db.session.commit()

    toppings = Topping.query.all()
    toppingList = ['None']
    for topping in toppings:
        toppingList.append(topping.name)
    return render_template('addPizza.html', toppings=toppings, toppingList=toppingList, no_sidebar=True)


# @views.route('/', methods=['GET', 'POST'])
# # @login_required
# def home():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
        

#     pizzas = Pizza.query.all()
#     toppings = Topping.query.all()
#     pizzaToppings = PizzaTopping.query.all()
#     # tomato_sauce = Topping.query.filter_by(name='Tomato sauce').first()
    

#     return render_template("home.html", pizzaToppings=pizzaToppings, toppings=toppings, pizzas=pizzas)


# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(first_name) < 2:
#             flash('First name must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = User(email=email, first_name=first_name, password=generate_password_hash(
#                 password1, method='sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             return redirect(url_for('views.home'))

#     return render_template("sign_up.html", user=current_user)





@views.route('/test', methods=['GET', 'POST'])
def test():

    comments = 'I suck at Flask'
    pizzas = Pizza.query.all()

    # if current_user.is_authenticated:
    #     return redirect(url_for('auth.regTest'))
    if request.method == 'POST':
        pass
  


    return render_template("test.html", comments=comments, pizzas=pizzas)






# @views.route("/post/<int:post_id>", methods=['GET', 'POST'])
# def thread(post_id):
#     form = CommentForm()
#     post = Post.query.get_or_404(post_id)
#     if form.validate_on_submit():
#         comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post_id)
#         # comment = Comment(content=form.content.data, post=post, author=current_user)
#         # {{ comment.author.name }}
#         db.session.add(comment)
#         db.session.commit()
#         myComment = form.content.data
#         flash('Your comment has been posted!', 'success-message')
#         # flash('This is a test message!', 'info')
#         return redirect(url_for('views.thread', post_id=post.id))
#     else:
#         myComment = 'wrong wrong wrong'    
#     return render_template('thread.html', title=post.title, post=post, form=form, myComment=myComment)




@views.route('/mydb', methods=['GET', 'POST'])
def mydb():

    comments = 'I suck at Flask'
    pizzas = Pizza.query.all()

    return render_template("mydb.html", comments=comments, pizzas=pizzas)



@views.route('/qqq', methods=['GET', 'POST'])
def qqq():

    comments = 'I suck at Flask'
    pizzas = Pizza.query.all()

    if request.method == 'POST':
        pass


    return render_template("qqq.html", comments=comments, pizzas=pizzas, no_sidebar=True)




@views.route('/stockTopping', methods=['GET', 'POST'])
def stockTopping():
    selected_pizza = None
    if request.method == 'POST':
        # submit = request.form.get('submit')
        submit = request.form.get('submit_pizza')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        if submit:
            
            if submit:
                topping_id = request.form.get('topping_id')
                inventory = request.form.get(f"{topping_id}_size")
                print(f"{topping_id=}")
                print(type(topping_id))
                print(f"{inventory=}")
                print(type(inventory))
                               
              


                topping_to_update = Topping.query.get(int(topping_id))
                # inventoryCapital = inventory.capitalize()
                # inventoryCapital = inventory.title()
                
                # i think i can remove this line ↓
                topping_to_update.inventory = inventory
                db.session.commit()
                flash(f"Topping inventory changed to {inventory}!", 'success')


        
        makeOrder = request.form.get('makeOrder')
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        if makeOrder == 'makeOrder':
            print('CCCCCCCCCCCCCCCCCCCCCCCC')
            orders = PizzaOrder.query.all()
            for order in orders:
                # print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
                # print(order)
                new_order = OrderHistory(name=order.name, size=order.size, price=order.price)
                db.session.add(new_order)
            db.session.commit()
            
    pizzas = Pizza.query.all()
    prices = PizzaPrice.query.all()
    toppings = Topping.query.all()
    orders = PizzaOrder.query.all()
    return render_template('stockTopping.html', pizzas=pizzas, selected_pizza=selected_pizza, prices=prices, toppings=toppings, orders=orders, is_in_stock=is_in_stock)





@views.route('/orderHistory', methods=['GET', 'POST'])
def orderHistoryg():
    selected_pizza = None
    if request.method == 'POST':
        # submit = request.form.get('submit')
        submit = request.form.get('submit_pizza')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        if submit:
            
            if submit:
                topping_id = request.form.get('topping_id')
                inventory = request.form.get(f"{topping_id}_size")
                print(f"{topping_id=}")
                print(type(topping_id))
                print(f"{inventory=}")
                print(type(inventory))
                               
              


                topping_to_update = Topping.query.get(int(topping_id))
                # inventoryCapital = inventory.capitalize()
                # inventoryCapital = inventory.title()
                topping_to_update.inventory = inventory
                db.session.commit()
                flash(f"Topping inventory changed to {inventory}!", 'success')


        
        makeOrder = request.form.get('makeOrder')
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        if makeOrder == 'makeOrder':
            print('CCCCCCCCCCCCCCCCCCCCCCCC')
            orders = PizzaOrder.query.all()
            for order in orders:
                # print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
                # print(order)
                new_order = OrderHistory(name=order.name, size=order.size, price=order.price)
                db.session.add(new_order)
            db.session.commit()
            
    pizzas = Pizza.query.all()
    prices = PizzaPrice.query.all()
    toppings = Topping.query.all()
    # orders = PizzaOrder.query.all()
    orders = OrderHistory.query.all()
    return render_template('orderHistory.html', pizzas=pizzas, selected_pizza=selected_pizza, prices=prices, toppings=toppings, orders=orders, is_in_stock=is_in_stock)


