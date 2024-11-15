from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
from forms import ProductForm, ProductTypeForm
from models import db, Product, ProductType


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/')
def index():
    filter_type = request.args.get('filter_type', type=str)
    if filter_type:
        products = Product.query.filter_by(type=filter_type).all()
    else:
        products = Product.query.all()
    product_types = ProductType.query.all()
    return render_template('index.html', products=products, product_types=product_types)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    product_types = ProductType.query.all()
    form.existing_type.choices = [(str(pt.id), pt.type) for pt in product_types]

    if form.validate_on_submit():
        if form.new_type.data:
            new_type = ProductType(type=form.new_type.data)
            db.session.add(new_type)
            db.session.commit()
            product_type = new_type
        else:
            product_type = ProductType.query.get(int(form.existing_type.data))

        filename = photos.save(form.image.data)

        product = Product(
            name=form.name.data,
            count=form.count.data,
            expired_date=form.expired_date.data,
            location=form.location.data,
            image=filename,
            type=product_type.type
        )

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_product.html', form=form, product_types=product_types)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    product_types = ProductType.query.all()
    form.existing_type.choices = [(str(pt.id), pt.type) for pt in product_types]

    if form.validate_on_submit():
        if form.new_type.data:
            new_type = ProductType(type=form.new_type.data)
            db.session.add(new_type)
            db.session.commit()
            product_type = new_type
        else:
            product_type = ProductType.query.get(int(form.existing_type.data))

        product.name = form.name.data
        product.count = form.count.data
        product.expired_date = form.expired_date.data
        product.location = form.location.data
        product.type = product_type.type

        if form.image.data:
            filename = photos.save(form.image.data)
            product.image = filename

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_product.html', form=form, product=product)

@app.route('/get_product_types', methods=['GET'])
def get_product_types():
    product_types = ProductType.query.all()
    return jsonify([{'id': pt.id, 'type': pt.type} for pt in product_types])

@app.route('/remove_product/<int:product_id>', methods=['GET', 'POST'])
def remove_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('remove_product.html', product=product)

@app.route('/update_count/<int:product_id>/<action>', methods=['POST'])
def update_count(product_id, action):
    product = Product.query.get_or_404(product_id)
    if action == 'add':
        product.count += 1
    elif action == 'subtract':
        product.count -= 1
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit_product_type/<int:type_id>', methods=['GET', 'POST'])
def edit_product_type(type_id):
    product_type = ProductType.query.get_or_404(type_id)
    form = ProductTypeForm(obj=product_type)

    if form.validate_on_submit():
        product_type.type = form.type.data
        db.session.commit()
        flash('Product type updated successfully.', 'success')
        return redirect(url_for('manage_product_types'))

    return render_template('edit_product_type.html', form=form, product_type=product_type)


@app.route('/manage_product_types')
def manage_product_types():
    product_types = ProductType.query.all()
    return render_template('manage_product_types.html', product_types=product_types)


@app.route('/remove_product_type/<int:type_id>')
def remove_product_type(type_id):
    product_type = ProductType.query.get_or_404(type_id)

    # Check if there are any products using this type
    products_with_type = Product.query.filter_by(type=product_type.type).first()

    if products_with_type:
        flash('Cannot remove this type as it is being used by one or more products.', 'error')
    else:
        db.session.delete(product_type)
        db.session.commit()
        flash('Product type removed successfully.', 'success')

    return redirect(url_for('manage_product_types'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
