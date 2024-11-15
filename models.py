from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    count = db.Column(db.Integer)
    expired_date = db.Column(db.Date)
    location = db.Column(db.String(120))
    type = db.Column(db.String(120))
    image = db.Column(db.String(120))

class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120), unique=True)
