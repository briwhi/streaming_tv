from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField


class ChannelForm(FlaskForm):
    name = StringField(label="Name")
    submit = SubmitField(label="Submit")
    
    
class TVForm(FlaskForm):
    name = StringField(label="Name")
    submit = SubmitField(label="Submit")
    
    
    