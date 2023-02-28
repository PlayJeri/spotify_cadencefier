from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import data_required

class PlayListForm(FlaskForm):
  playlist_name = StringField('Name your playlist', validators=[data_required()])
  genre = StringField('What genre would you like?', validators=[data_required()])
  tempo_min = IntegerField(label='What is your preferred min cadence?')
  tempo_max = IntegerField(label='What is your preferred max cadence?')
  submit = SubmitField()
