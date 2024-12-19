from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, NumberRange
from .models import Product
from . import db

# Define the admin blueprint
admin = Blueprint('admin', __name__)

# Define the form
class AddItemForm(FlaskForm):
    """Form for adding items to the shop."""
    name = StringField('Name', validators=[DataRequired(message="Name is required.")])

    description = StringField('Description', validators=[DataRequired(message="Description is required.")])

    price = FloatField('Price', validators=[
        InputRequired(message="Price is required."),
        NumberRange(min=0, message="Price must be a positive number.")
    ])

    stock_quantity = IntegerField('Stock Quantity', validators=[
        InputRequired(message="Stock quantity is required."),
        NumberRange(min=0, message="Stock quantity must be a non-negative number.")
    ])

    brand = StringField('Brand', validators=[DataRequired(message="Brand is required.")])
    
    category = StringField('Category', validators=[DataRequired(message="Category is required.")])
    
    updated_at = DateTimeField('Updated At')  # Optional; pre-filled if not provided
    
    rating = FloatField('Rating', validators=[
        NumberRange(min=0, max=5, message="Rating must be between 0 and 5.")
    ])
    
    ratting = StringField('Ratting', validators=[DataRequired(message="Ratting is required.")])

# Define the route to add shop items
@admin.route('/add-shop-items', methods=['POST'])
def add_shop_items():
    form = AddItemForm(meta={'csrf': False})  # Disable CSRF for API requests

    if not form.validate_on_submit():
        return jsonify({'message': 'Validation failed', 'errors': form.errors}), 400

    try:
        # Create a new product from form data
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data,
            brand=form.brand.data,
            category=form.category.data,
            updated_at=form.updated_at.data if form.updated_at.data else datetime.utcnow(),
            rating=form.rating.data,
            ratting=form.ratting.data
        )

        # Add the product to the database
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        db.session.rollback()  # Rollback transaction in case of error
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        db.session.close()  # Ensure the session is closed


# Define the route to remove shop items
@admin.route('/remove-shop-items/<int:product_id>', methods=['DELETE'])
@login_required
def remove_shop_items(product_id):
    try:
        # Query the product by ID
        product = Product.query.get(product_id)

        # Check if the product exists
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        # Remove the product from the database
        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product removed successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback transaction in case of error
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        db.session.close()  # Ensure the session is closed