from flask import Flask, render_template, redirect, url_for, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
from forms import ProductForm
from models import db, Product

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        product = Product(
            name=form.name.data,
            count=form.count.data,
            expired_date=form.expired_date.data,
            location=form.location.data,
            image=filename
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)

@app.route('/remove_product', methods=['GET', 'POST'])
def remove_product():
    form = ProductForm()
    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        product = Product(
            name=form.name.data,
            count=form.count.data,
            expired_date=form.expired_date.data,
            location=form.location.data,
            image=filename
        )
        db.session.remove(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('remove_product.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
