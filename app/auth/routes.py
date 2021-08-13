import flask
from app import (db)
from flask import (render_template, redirect, url_for, flash, request)
from flask_login import (current_user, login_user, logout_user, login_required)
from werkzeug.urls import url_parse
from app.auth import bp
from app.auth.forms import (LoginForm, RegistrationForm)
from app.models import (User)
from app.__init__ import (technologiesUtilisees, plus_longue_liste_techno)


@bp.route("/Login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.accueil'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.connexion'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        flash("Bienvenue, "+ current_user.username + " !", 'success')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.accueil')
        return redirect(next_page)
   
    return render_template('auth/connexion.html', title='Sign In', form=form,
    technologiesUtilisees = technologiesUtilisees,
    plus_longue_liste_techno=plus_longue_liste_techno)


@bp.route("/Register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.accueil'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
   
    return render_template('auth/inscription.html', title='Register',
    form=form,
    technologiesUtilisees = technologiesUtilisees,
    plus_longue_liste_techno=plus_longue_liste_techno)


@bp.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('main.accueil'))