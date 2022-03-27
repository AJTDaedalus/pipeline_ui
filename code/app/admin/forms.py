from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, InputRequired, \
                               Length
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from app.models import User, Role


class NewRoleForm(FlaskForm):
    """
    Form for creating new roles.
    """
    name = StringField('Role name', validators=[InputRequired(), Length(1,64)])
    create = SubmitField('Create new role')

class AssignRoleForm(FlaskForm):
    """
    Form for assigning roles to users.
    """
    user = QuerySelectField('Select user to assign role(s) to.',
                            query_factory=lambda: User.query,
                            get_label = 'email')
    new_roles = QuerySelectMultipleField('Select one or more roles to assign.',
                                     query_factory=lambda: Role.query,
                                     get_label = 'name')
    assign = SubmitField('Assign role(s) to user')

class RemoveRoleForm(FlaskForm):
    """
    Form for removing roles from users.
    """
    user = QuerySelectField('Select user to remove role(s) from.',
                            query_factory=lambda: User.query,
                            get_label = 'email')
    rem_roles = QuerySelectMultipleField('Select one or more roles to remove.',
                                     query_factory=lambda: Role.query,
                                     get_label = 'name')
    remove = SubmitField('Remove role(s) to user')
