from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp

class ProjectForm(Form):
    project_name = StringField('Project Name', validators=[Required()])
    submit = SubmitField('Submit')
