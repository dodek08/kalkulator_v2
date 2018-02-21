from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Optional

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SimpleForm(Form):
    string_of_files = ['one\r\ntwo\r\nthree\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)

class DodajOkreg(FlaskForm):
    lokalizacja = StringField('Lokalizacja', validators=[DataRequired()])
    komisarz = StringField('Komisarz', validators=[DataRequired()])
    submit = SubmitField('Dodaj')


class EdytujOkreg(FlaskForm):
    idokregu = IntegerField('Numer okręgu',validators=[DataRequired()])
    noweidokregu = IntegerField('Nowy numer okręgu',validators=[Optional()])
    lokalizacja = StringField('Nowa lokalizacja', validators=[Optional()])
    komisarz = StringField('Nowy komisarz', validators=[Optional()])
    submit = SubmitField('Zmień')


class DodajKomitet(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    submit = SubmitField('Dodaj')

class EdytujKomitet(FlaskForm):
    id = IntegerField('Numer listy',validators=[DataRequired()])
    noweid = IntegerField('Nowy numer listy',validators=[Optional()])
    nazwa = StringField('Nazwa', validators=[Optional()])
    submit = SubmitField('Zmień')

class DodajKandydata(FlaskForm):
    imie = StringField('Imię', validators=[DataRequired()])
    nazwisko = StringField('Nazwisko', validators=[DataRequired()])
    numer_listy = IntegerField('Numer listy', validators=[DataRequired()])
    submit = SubmitField('Dodaj')

class EdytujKandydata(FlaskForm):
    id = IntegerField('ID kandydata',validators=[DataRequired()])
    imie = StringField('Nowe imię', validators=[Optional()])
    nazwisko = StringField('Nowe nazwisko', validators=[Optional()])
    numer_listy = IntegerField('Nowy numer listy', validators=[Optional()])
    noweid = IntegerField('Nowe ID kandydata', validators=[Optional()])
    submit = SubmitField('Zmień')

class OkregZaloguj(FlaskForm):
    numer = IntegerField('Numer okręgu',validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

class DodajObwod(FlaskForm):
    lokalizacja = StringField('Lokalizacja', validators=[DataRequired()])
    imie = StringField('Imię przewodniczącego', validators=[DataRequired()])
    nazwisko = StringField('Nazwisko przewodniczącego', validators=[DataRequired()])
    afiliacja = StringField('Afiliacja przewodniczącego', validators=[Optional()])
    submit = SubmitField('Dodaj')

class EdytujObwod(FlaskForm):
    id = IntegerField('Numer obwodu',validators=[DataRequired()])
    noweid = IntegerField('Nowy numer obwodu',validators=[Optional()])
    noweidokregu = IntegerField('Nowy numer okręgu',validators=[Optional()])
    imie = StringField('Nowe imię przewodniczącego', validators=[Optional()])
    nazwisko = StringField('Nowe nazwisko przewodniczącego', validators=[Optional()])
    afiliacja = StringField('Nowa afiliacja przewodniczącego', validators=[Optional()])
    lokalizacja = StringField('Nowa lokalizacja', validators=[Optional()])
    submit = SubmitField('Dodaj')

class ObwodZaloguj(FlaskForm):
    numer = IntegerField('ID członka komisji',validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

class DodajGlosy(FlaskForm):
    id = IntegerField('ID kandydata',validators=[DataRequired()])
    glosy = IntegerField('Liczba głosów',validators=[DataRequired()])
    submit = SubmitField('Dodaj')

class Usun(FlaskForm):
    id = IntegerField('Nazwa', validators=[DataRequired()])
    submit = SubmitField('Dodaj')