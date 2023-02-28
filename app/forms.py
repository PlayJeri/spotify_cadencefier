from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerRangeField, RadioField
from wtforms.validators import data_required

class PlayListForm(FlaskForm):
  playlist_name = StringField('Name your playlist', validators=[data_required()])
  genre_or_artist = RadioField('Add by genre or artist?', choices=['Genre', 'Artist'])
  genre = StringField('What genre / artist would you like?', validators=[data_required()])
  tempo = IntegerRangeField('Select wanted cadence', default=115)
  submit = SubmitField()
