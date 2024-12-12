from datetime import datetime
from flask_login import UserMixin
# from flask import current_app
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from website import db, login_manager

"""
I messed up the relationships and figured it out to late so making changes meant i had to change alot of code which proved to be tricky. The setup i have now i found did not work with cascades either so i had to remove records manually. 
"""


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
 

class Pizza(db.Model):
    __tablename__ = "pizza"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    
class Topping(db.Model):
    __tablename__ = "topping"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    inventory = db.Column(db.Enum('nothing', 'little', 'modest', 'plenty'), default='plenty')


class PizzaTopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    name = db.Column(db.String(20))
    pizza = db.relationship('Pizza', backref='toppings')
    
    def __repr__(self):
        return f"('{self.name}')"
    
    
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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Order ID {self.orderID}, {self.name}, {self.size}, {self.price}kr, ({self.date.strftime('%Y-%m-%d %H:%M')}) - Order price: {self.totalPrice}kr"


