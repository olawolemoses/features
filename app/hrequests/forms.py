from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Feature, User, Client, ProductArea, Project
from wtf_tinymce.forms.fields import TinyMceField

class FeatureForm(Form):
    title = StringField('Title', validators=[Required()])
    description = TextAreaField('Description', validators=[Required()])
    client_priority = SelectField('Client Priority', validators=[Required()],coerce=int, default=None)
    target_date = DateField('Target Date', format="%m/%d/%Y", validators=[Required()])
    product_area = SelectField('Product Area', coerce=int, validators=[Required()], default=None)
    user_id =  IntegerField("", widget=HiddenInput() )
    client = SelectField('Client', coerce=int, validators=[Required()], default=(None, '--'))
    project = SelectField('Project', coerce=int, validators=[Required()], default=None)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(FeatureForm, self).__init__(*args, **kwargs)
        self.client.choices = [(0, 'Please Select')] + [(client.id, client.client_name) for client in Client.query.order_by(Client.client_name).all()]
        self.project.choices = [(0, 'Please Select')] + [(project.id, project.project_name) for project in Project.query.order_by(Project.project_name).all()]
        self.product_area.choices = [(0, 'Please Select')] + [(pa.id, pa.product_area) for pa in ProductArea.query.order_by(ProductArea.product_area).all()]
        self.client_priority.choices = get_client_priority()
        #[('', 'Please Select'), ('1', 'low'), ('2', 'medium'), ('3', 'High')]

def get_client_priority():
    choices = [ (x, x) for x in range(1, Feature.query.count() + 1) ]
    if len(choices) < 1:
        choices = [ (1,1) ]
    return [(0, 'Please Select')] + choices
