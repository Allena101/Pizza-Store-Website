from website import create_app
from website import db # for inserting example data
from website.models import User, Pizza, PizzaPrice, Topping # for inserting example data
from website.sampleData import load_example_data # for inserting example data




app = create_app()

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    #     load_example_data()
    app.run(debug=True)



