from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired()])
    expired_date = DateField('Expired Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image = FileField('Product Image', validators=[DataRequired()])
