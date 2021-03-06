from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField


class ChannelForm(FlaskForm):
    name = StringField(label="Name")
    submit = SubmitField(label="Submit")
    
    
class TVForm(FlaskForm):
    name = StringField(label="Name")
    monthly_price = DecimalField(places=2)
    submit = SubmitField(label="Submit")
    
    
    