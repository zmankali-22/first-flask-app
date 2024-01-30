

from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://new_database_dev:123456@localhost:5432/new_database"

db = SQLAlchemy(app)
ma= Marshmallow(app)

# create table

class Product(db.Model):
    __tablename__= "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer)
    description = db.Column(db.String(1000))

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price','stock', 'description')

products_schema = ProductSchema(many=True)
product_schema = ProductSchema(many=False)

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
    # convert to JSON

    data = products_schema.dump(product_list)
    return data

@app.route('/products/<int:product_id>')
def get_product(product_id):
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if(product):

        data = product_schema.dump(product)
        return data
    else:
        return {'message': 'Product not found'}, 404


@app.route('/products', methods= ['POST'])
def create_product():
    product_fields = request.get_json()
    new_product = Product(
        name = product_fields.get("name"),
        price = product_fields.get("price"),
        stock = product_fields.get("stock"),
        description= product_fields.get("description")
        
    )
    
    db.session.add(new_product)
    db.session.commit()
    data = product_schema.dump(new_product)
    return data, 201







@app.route('/')
def hello_world():
    return 'Hello World!'