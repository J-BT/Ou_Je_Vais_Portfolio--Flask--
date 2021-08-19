import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/ou_je_vais.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Ou je vais startup')
        
    return app

technologiesUtilisees = {
            "frontend" : ["HTML", "CSS", "Javascript", "Bootstrap",
             "jQuery","Chart.js","Anime.js", "Alertify.js"],
            "backend" : ["Python", "Flask", "Pandas","Jupyter",
             "Seaborn", "Matplotlib","Numpy"],
            "bdd" : ["PostgreSQL", "SQLAlchemy", "PgAdmin"],
            "serveur" : ["Digital Ocean", "Ubuntu Server",
             "NGINX", "Git", "GitHub"]
        }
nb_elements_max = max(len(technologie) \
        for technologie in technologiesUtilisees.values())
plus_longue_liste_techno = [technologie \
    for technologie in technologiesUtilisees.values() \
        if len(technologie) == nb_elements_max]
plus_longue_liste_techno = plus_longue_liste_techno[0]


from app import models, data_mining, data_visualization