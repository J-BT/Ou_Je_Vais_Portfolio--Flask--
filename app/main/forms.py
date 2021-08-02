from flask_wtf import FlaskForm
from wtforms import (SubmitField, SelectField)


class Choix_utilisateur(FlaskForm):
    nombre_population = SelectField(
        'Population') 
    esperance_vie = SelectField(
        'Esperance de Vie')
    taux_chomage = SelectField(
        'Taux de Chômage')  
    temperature = SelectField(
        'Temperature')  
    meteo = SelectField(
        'Météo') 
    choix_submit = SubmitField(
        'Soumettre')
    
    