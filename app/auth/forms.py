from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
 BooleanField, SubmitField, SelectField)
from wtforms.validators import (ValidationError, DataRequired, Email, EqualTo)
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Nom', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se rappeler de moi')
    submit = SubmitField('Se connecter')


class RegistrationForm(FlaskForm):
    username = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField(
        'Répéter le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Choisissez un autre nom s\'il vous plait')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Choisissez une autre adresse s\'il vous plait')