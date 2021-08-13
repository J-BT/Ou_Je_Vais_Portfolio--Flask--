from flask import render_template
from app import db
from app.errors import bp
from app.__init__ import (technologiesUtilisees,plus_longue_liste_techno)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html',
    technologiesUtilisees = technologiesUtilisees,
    plus_longue_liste_techno=plus_longue_liste_techno), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html',
    technologiesUtilisees = technologiesUtilisees,
    plus_longue_liste_techno=plus_longue_liste_techno), 500
