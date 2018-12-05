from wtforms.validators import ValidationError

class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field

        if not message:
            message = u'this element already exists'

        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if 'id' in form:
            id = form.id.data
        else:
            id = None
        if check and (id is None or id != check.id):
            raise ValidationError(self.message)
