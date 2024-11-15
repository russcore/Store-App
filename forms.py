from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed, FileRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired()])
    expired_date = DateField('Expired Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    existing_type = SelectField('Existing Type', validators=[Optional()])
    new_type = StringField('New Type', validators=[Optional()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'), Optional()])


class ProductTypeForm(FlaskForm):
    existing_type = SelectField('Existing Type', validators=[Optional()])
    new_type = StringField('New Type', validators=[Optional()])


class ProductTypeForm(FlaskForm):
    type = StringField('Type Name', validators=[DataRequired()])