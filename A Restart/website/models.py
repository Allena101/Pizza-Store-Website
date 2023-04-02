from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# from website import db, login_manager, bcrypt
# from website import bcrypt
from website import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



# class Pizza(db.Model):
#     __tablename__ = "pizza"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
    
    # topping_ids = db.Column(db.Integer, db.ForeignKey('topping.id'))
    # topping_id = db.Column(db.Integer, nullable=False)
    # toppings = db.relationship('Topping', backref='pizza', lazy=True)
    
    
    # def __repr__(self):
    #     return f"('{self.name}' has these toppings: '{self.topping_id}')"
    

class Pizza(db.Model):
    __tablename__ = "pizza"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # topping_ids = db.Column(db.Integer, db.ForeignKey('topping.id'))
    # toppings = db.relationship('Topping', backref='pizza', lazy=True)
    
    # def __repr__(self):
    #     return f"('{self.name}' has these toppings: '{self.toppings}')"


    
class Topping(db.Model):
    __tablename__ = "topping"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    inventory = db.Column(db.Enum('nothing', 'little', 'medium', 'plenty'), default='plenty')
    # change medium to modest (you have to change in the sampleData.py)
    # change to capital letters - get it working first!

class PizzaTopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    name = db.Column(db.String(20))
    pizza = db.relationship('Pizza', backref='toppings')
    
    def __repr__(self):
        return f"('{self.name}')"
    
    
    
# class PizzaPrice(db.Model):
#     __tablename__ = "pizza_price"
#     id = db.Column(db.Integer, primary_key=True)
#     pizza = db.Column(db.String, nullable=False)
#     size = db.Column(db.Enum('Small', 'Medium', 'Large'), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     sale = db.Column(db.Boolean, default=False)
    
    
# class PizzaPrice(db.Model):
#     __tablename__ = "pizza_price"
#     id = db.Column(db.Integer, primary_key=True)
#     pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
#     size = db.Column(db.Enum('Small', 'Medium', 'Large'), nullable=False, default='Medium')
#     price = db.Column(db.Integer, nullable=False)
#     sale = db.Column(db.Boolean, default=False)

#     def __repr__(self):
#         return f"('{self.pizza_id}', '{self.size}', '{self.price}', '{self.sale}')"
    
    
class PizzaPrice(db.Model):
    __tablename__ = "pizza_price"
    id = db.Column(db.Integer, primary_key=True)
    pizza = db.Column(db.String, nullable=False)
    size = db.Column(db.Enum('Small', 'Medium', 'Large'), nullable=False)
    _price = db.Column('price', db.Integer, nullable=False)
    sale = db.Column(db.Boolean, default=False)

    @property
    def price(self):
        if self.size == 'Small':
            return int(self._price * 0.8)
        elif self.size == 'Large':
            return int(self._price * 1.2)
        else:
            return self._price

    @price.setter
    def price(self, value):
        self._price = value

    
    
    # # Create a pizza instance
    # my_pizza = Pizza(name='Pepperoni')
    # db.session.add(my_pizza)
    # db.session.commit()

    # # Create a pizza price instance
    # my_pizza_price = PizzaPrice(pizza='Pepperoni', size='Medium', price=100)
    # db.session.add(my_pizza_price)
    # db.session.commit()


class PizzaOrder(db.Model):
    __tablename__ = "pizza_order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Enum('Small', 'Medium', 'Large'),default='Medium', nullable=False)
    price = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"{self.name}, {self.size}, {self.price}kr"
    
class OrderHistory(db.Model):
    __tablename__ = "order_history"
    id = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Enum('Small', 'Medium', 'Large'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Order ID {self.orderID}, {self.name}, {self.size}, {self.price}kr - Order price {self.totalPrice}kr"


