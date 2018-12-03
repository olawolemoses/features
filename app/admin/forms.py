from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Role


class RoleForm(Form):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[Required()])
    description = StringField('Description', validators=[Required()])
    submit = SubmitField('Submit')

class UserAssignForm(Form):
    """
    Form for admin roles to users
    """
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')
