from website.models import db, User, Pizza, Topping, PizzaPrice, PizzaTopping
from datetime import datetime

def load_example_data():
    
    # # create users
    # These users will not work on the site because the password does not get hashed.
    user1 = User(username='Alice', email='alice@example.com', password='password')
    user2 = User(username='Bob', email='bob@example.com', password='password')
    user3 = User(username='Charlie', email='charlie@example.com', password='password')

    # add users to session and commit to database
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    toppings = [
    Topping(name='Tomatoe'),
    Topping(name='Cheese'),
    Topping(name='Pepperoni'),
    Topping(name='Pineapple'),
    Topping(name='Mushrooms'),
    Topping(name='Olives'),
    Topping(name='Peppers'),
    Topping(name='Shrimp'),
    Topping(name='Crab'),
    Topping(name='Tuna'),
    Topping(name='Bacon', inventory='nothing'),
    Topping(name='Egg'),
    Topping(name='Artichokes'),
    Topping(name='Gorgonzola'),
    Topping(name='Parmesan'),
    Topping(name='Emmental'),
    Topping(name='Anchovies'),
    Topping(name='Capers'),
    Topping(name='Ham'),
    Topping(name='Fish'),
    ]

    db.session.add_all(toppings)
    db.session.commit()
    
    
    
    margherita_pizza = Pizza(name='Margherita')
    pepperoni_pizza = Pizza(name='Pepperoni')
    hawaii_pizza = Pizza(name='Hawaii')
    
    db.session.add(margherita_pizza)
    db.session.add(pepperoni_pizza)
    db.session.add(hawaii_pizza)
    db.session.commit()

    # Create instances of toppings
    top1 = PizzaTopping(name='Cheese', pizza_id=1)
    top2 = PizzaTopping(name='Tomatoe', pizza_id=1)
    top3 = PizzaTopping(name='Fish', pizza_id=2)
    top4 = PizzaTopping(name='Tomatoe', pizza_id=2)
    top5 = PizzaTopping(name='Bacon', pizza_id=2)
    top6 = PizzaTopping(name='Bacon', pizza_id=3)
    top7 = PizzaTopping(name='Cheese', pizza_id=3)

    # Add the toppings to the session and commit to database
    db.session.add(top1)
    db.session.add(top2)
    db.session.add(top3)
    db.session.add(top4)
    db.session.add(top5)
    db.session.add(top6)
    db.session.add(top7)
    db.session.commit()
    

    # Add Margherita prices
    margherita_small = PizzaPrice(pizza='Margherita', size='Small', price=100)
    db.session.add(margherita_small)

    margherita_medium = PizzaPrice(pizza='Margherita', size='Medium', price=100)
    db.session.add(margherita_medium)

    margherita_large = PizzaPrice(pizza='Margherita', size='Large', price=100)
    db.session.add(margherita_large)

    # Add Pepperoni prices
    pepperoni_small = PizzaPrice(pizza='Pepperoni', size='Small', price=110)
    db.session.add(pepperoni_small)

    pepperoni_medium = PizzaPrice(pizza='Pepperoni', size='Medium', price=130)
    db.session.add(pepperoni_medium)

    pepperoni_large = PizzaPrice(pizza='Pepperoni', size='Large', price=150)
    db.session.add(pepperoni_large)

    # Add Hawaii prices
    hawaii_small = PizzaPrice(pizza='Hawaii', size='Small', price=120)
    db.session.add(hawaii_small)

    hawaii_medium = PizzaPrice(pizza='Hawaii', size='Medium', price=140)
    db.session.add(hawaii_medium)

    hawaii_large = PizzaPrice(pizza='Hawaii', size='Large', price=160)
    db.session.add(hawaii_large)

    db.session.commit()

    
    
    
    
