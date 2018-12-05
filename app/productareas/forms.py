from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp

class ProductAreaForm(Form):
    product_area = StringField('Product Area', validators=[Required()])
    submit = SubmitField('Submit')
