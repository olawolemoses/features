from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Feature, User, Client, ProductArea, Project

class FeatureForm(Form):
    title = StringField('Title', validators=[Required()])
    description = StringField('Description', validators=[Required(), Length(1, 64)])
    client_priority = SelectField('Client Priority', validators=[Required()],coerce=int, default=None)
    target_date = DateField('Target Date', format="%m/%d/%Y", validators=[Required()])
    product_area = SelectField('Product Area', coerce=int, validators=[Required()], default=None)
    #user_id = StringField('User', validators=[Required(), Length(1, 64)])
    client = SelectField('Client', coerce=int, validators=[Required()], default=(None, '--'))
    project = SelectField('Project', coerce=int, validators=[Required()], default=None)
    user = SelectField('User', coerce=int, default=None)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(FeatureForm, self).__init__(*args, **kwargs)
        self.user.choices =[(0, 'Please Select')] +  [(user.id, user.username) for user in User.query.order_by(User.username).all()]
        self.client.choices = [(0, 'Please Select')] + [(client.id, client.client_name) for client in Client.query.order_by(Client.client_name).all()]
        self.project.choices = [(0, 'Please Select')] + [(project.id, project.project_name) for project in Project.query.order_by(Project.project_name).all()]
        self.product_area.choices = [(0, 'Please Select')] + [(pa.id, pa.product_area) for pa in ProductArea.query.order_by(ProductArea.product_area).all()]
        self.client_priority.choices = [(0, 'Please Select')] + [ (x, x) for x in range(1, Feature.query.count() + 1) ]
        #[('', 'Please Select'), ('1', 'low'), ('2', 'medium'), ('3', 'High')]
