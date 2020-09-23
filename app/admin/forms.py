from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CennikEdit(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    przedzial1 = IntegerField('Przedzial 1', validators=[DataRequired()])
    przedzial2 = IntegerField('Przedzial 2', validators=[DataRequired()])
    cena1 = IntegerField('Cena 1', validators=[DataRequired()])
    cena2 = IntegerField('Cena 2', validators=[DataRequired()])
    submit = SubmitField('Zapisz')
