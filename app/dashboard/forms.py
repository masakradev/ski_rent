from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, HiddenField, FieldList, FormField, DecimalField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired

class WypozyczeniePozycja(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(meta={'csrf':False}, *args, **kwargs)

    key = HiddenField('key')
    nazwa = StringField('Nazwa')
    ean = StringField('EAN')
    rozmiar = StringField('Rozmiar')
    cena = IntegerField('Cena')



class WypozyczenieDodaj(FlaskForm):
    klient_nazwa = StringField('Imie i nazwisko', validators=[DataRequired()])
    klient_dowod = StringField('Seria i nr dowodu', validators=[DataRequired()])
    klient_nr_tel = StringField('Numer telefonu', validators=[DataRequired()])
    wypozyczenie_od = DateField('Wypozyczenie od', validators=[DataRequired()])
    wypozyczenie_do = DateField('Wypozyczenie do', validators=[DataRequired()])
    wypozyczenie_od_godz = TimeField('Od godziny', validators=[DataRequired()])
    wypozyczenie_do_godz = TimeField('Do godziny', validators=[DataRequired()])
    cena = IntegerField('Cena')
    dodaj = StringField('Dodaj pozycje')
    pozycje_form = FieldList(FormField(WypozyczeniePozycja))

    submit = SubmitField('Dalej')