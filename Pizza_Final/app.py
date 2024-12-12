from website import create_app

from website import db  # for inserting example data
from website.models import (
    User,
    Pizza,
    PizzaPrice,
    Topping,
)  # for inserting example data
from website.sampleData import load_example_data  # for inserting example data

"""
I decided to leave the code in for the load in some sample data. It works if you get an invalidaiton on email unique constraint, which is as it should. Though I did not manage to figure out why the script tries to run add those record more than once.

"""


app = create_app()

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    #     load_example_data()
    # app.run(debug=True)
    app.run(debug=False)

# change file name from main.py to app.py
