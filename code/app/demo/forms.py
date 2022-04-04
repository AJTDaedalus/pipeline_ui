from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class DemoForm(FlaskForm):
    """
    Form to display demo page.
    """
    name = StringField('Demo message', validators=[InputRequired(), Length(1,64)])
    submit = SubmitField('Submit Demo Message')
