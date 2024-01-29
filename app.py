

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://new_database_dev:123456@localhost:5432/new_database"

db = SQLAlchemy(app)

# create table

class Product(db.Model):
    __tablename__= "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer)
    description = db.Column(db.String(1000))



# cli command
    
@app.cli.command("create")
def create_table():
    db.create_all()
    print("Table created")

@app.cli.command("insert")
def insert_data():
    product1 = Product( name="Product 1", price=100, stock = 15, description="This is product 1")
    product2 = Product( name="Product 2", price=200, stock = 16, description="This is awesome prodcution product")

    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()
    print("Data inserted")


@app.cli.command("drop")
def drop_table():
    db.drop_all()
    print("Table dropped")

#  route to all products

@app.route('/products')
def get_products():
    stmt = db.select(Product)
    product_list = db.session.scalars(stmt)
    return product_list










@app.route('/')
def hello_world():
    return 'Hello World!'