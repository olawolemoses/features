from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp

class ClientForm(Form):
    client_name = StringField('Client Name', validators=[Required()])
    submit = SubmitField('Submit')
