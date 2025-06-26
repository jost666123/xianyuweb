from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True) # URL or path to image
    purchase_url = db.Column(db.String(500), nullable=True)
    purchase_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    selling_url = db.Column(db.String(500), nullable=True)
    selling_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    profit = db.Column(db.Numeric(10, 2), nullable=True, default=0.0) # Can be calculated: selling_price - purchase_price
    exposure = db.Column(db.Integer, nullable=True, default=0)
    sales_count = db.Column(db.Integer, nullable=True, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.id}: {self.title}>'

    def calculate_profit(self):
        if self.selling_price is not None and self.purchase_price is not None:
            self.profit = self.selling_price - self.purchase_price
        else:
            self.profit = 0.0
        return self.profit

# Example of how to use it with Flask app (will be in app.py)
# from flask import Flask
# from .config import DATABASE_URI
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
#
# with app.app_context():
#     db.create_all() # To create tables
#
#     # Example usage:
#     # new_product = Product(title="Test Product", purchase_price=10.0, selling_price=25.0)
#     # new_product.calculate_profit()
#     # db.session.add(new_product)
#     # db.session.commit()
#     #
#     # products = Product.query.all()
#     # print(products)
