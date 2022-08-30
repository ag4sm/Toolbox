from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class NewToolForm(FlaskForm):
    tool_name = StringField('Tool Name', validators=[DataRequired()])
    tool_brand = StringField('Tool Brand', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Tool')
