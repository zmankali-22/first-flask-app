

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://new_database_dev:123456@localhost:5432/new_database"

db = SQLAlchemy(app)

# create table

class Product(db.Model):
    __tablename__= "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100) nullable=False)
    price = db.Column(db.Integer nullable=False)
    stock = db.Column(db.Integer)
    description = db.Column(db.String(1000))



# cli command
    
@app.cli.command()
def create_table():
    db.create_all()
    print("Table created")

@app.cli.command()
def drop_table():
    db.drop_all()
    print("Table dropped")













@app.route('/')
def hello_world():
    return 'Hello World!'