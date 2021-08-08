from flask_wtf import FlaskForm
from wtforms import (SubmitField, SelectField)


class Choix_utilisateur(FlaskForm):
    nombre_population = SelectField(
        'Population', render_kw={'class': 'formulaireFlaskPreferences'}) 
    esperance_vie = SelectField(
        'Esperance de Vie', render_kw={'class': 'formulaireFlaskPreferences'})
    taux_chomage = SelectField(
        'Taux de Chômage', render_kw={'class': 'formulaireFlaskPreferences'})  
    temperature = SelectField(
        'Temperature', render_kw={'class': 'formulaireFlaskPreferences'})  
    meteo = SelectField(
        'Météo', render_kw={'class': 'formulaireFlaskPreferences'}) 
    choix_submit = SubmitField(
        'J\'y vais !')
    
    