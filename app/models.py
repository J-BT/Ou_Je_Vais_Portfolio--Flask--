from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from app import (db, login, engine)

from app.data_mining import (
    get_population,
    get_unemployment_rate,
    get_life_expectancy,
    get_temperature,
    get_timestamp_for_5_days,
    get_historical_5_previous_days,
    get_countries_populated
    )


class Message_user(db.Model):
    __tablename__ = 'message_user'

    id_msg_u = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    contenu = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender = db.relationship('User', backref='msg_sender', lazy='dynamic')

    def __repr__(self):
        return 'f<Message_User {self.username}, {self.contenu}>'


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    msg_user = db.Column(db.Integer, db.ForeignKey(
        'message_user.id_msg_u'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

    def __repr__(self):
        return f'<User {self.username}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Weather_5days(db.Model):
    id_weather_5days = db.Column(db.Integer, primary_key=True)
    weather_5days_country = db.Column(db.String(120))
    weather_5days_city = db.Column(db.String(120))
    weather_5days_date = db.Column(db.DateTime)
    weather_5days_w_id = db.Column(db.Integer)
    weather_5days_w_main = db.Column(db.String(120))
    weather_5days_w_descrip = db.Column(db.String(120))
    temp_5days_relation = db.relationship(
        'Country', backref='weather_5j_etudie', lazy='joined')
       
    def __repr__(self):
        return 'f<Weather_5days {self.weather_5days_country,\
            self.weather_5days_date, self.weather_5days_w_main }>'

    def populate():
        temperatures_5days, weather_5days = get_historical_5_previous_days()
        weather_5days  = weather_5days.to_sql(
        'weather_5days',
        con=db.engine,
        if_exists='append',
        index=False)
        print("Weather_5days populated")
        return "done"

    def delete():
        Weather_5days.__table__.drop(engine)
        print("Weather_5days deleted")
        return 'done'



class Temperature_5days(db.Model):
    id_temp_5days = db.Column(db.Integer, primary_key=True)
    temp_5days_country = db.Column(db.String(120))
    temp_5days_city = db.Column(db.String(120))
    temp_5days_date = db.Column(db.DateTime)
    temp_5days_value = db.Column(db.Float)
    temp_5days_relation = db.relationship(
        'Country', backref='temp_5j_etudiee', lazy='joined')
      
    def __repr__(self):
        return 'f<Temperature_5days {self.temp_5days_country,\
            self.temp_5days_date, self.temp_5days_value }>'
    
    def populate():
        temperatures_5days, weather_5days = get_historical_5_previous_days()
        temperatures_5days  = temperatures_5days.to_sql(
        'temperature_5days',
        con=db.engine,
        if_exists='append',
        index=False)
        print("Temperature_5days populated")
        return "done"

    def delete():
        Temperature_5days.__table__.drop(engine)
        print("Temperature_5days deleted")
        return 'done'

class Temperature(db.Model):
    id_temperature = db.Column(db.Integer, primary_key=True)
    temp_country = db.Column(db.String(120))
    temp_today = db.Column(db.DateTime)
    temp_value = db.Column(db.Float)
    pop_relation = db.relationship(
        'Country', backref='temp_etudie', lazy='joined')
        
    def __repr__(self):
        return 'f<Temperature {self.temp_country,\
            self.temp_today, self.temp_value }>'

    def populate():
        temperature = get_temperature()
        temp_frame = temperature
        temperature = temperature.to_sql(
                'temperature',
                con=db.engine,
                if_exists="append",
                index=False)
        print("Temperature populated")
        return "done"

    def delete():
        Temperature.__table__.drop(engine)
        print("Temperature deleted")
        return 'done'

class Population(db.Model):
    id_population = db.Column(db.Integer, primary_key=True)
    pop_country = db.Column(db.String(120))
    pop_year = db.Column(db.Integer)
    pop_value = db.Column(db.Integer)
    pop_relation = db.relationship(
        'Country', backref='pop_etudie', lazy='joined')
         
    def __repr__(self):
        return 'f<Population {self.pop_country,\
            self.pop_year, self.pop_value }>'

    def populate():
        colonnes_pop = ['pop_country','pop_year','pop_value']
        population = get_population()
        population.columns = colonnes_pop
        population = population.to_sql(
                'population',
                con=db.engine,
                if_exists="append",
                index=False)
        print("Population populated")
        return "done"

    def delete():
        Population.__table__.drop(engine)
        print("Population deleted")
        return 'done'

class Life_expectancy(db.Model):
    id_life_expe = db.Column(db.Integer, primary_key=True)
    l_e_country = db.Column(db.String(120))
    l_e_year = db.Column(db.Integer)
    l_e_value = db.Column(db.Float)
    l_e_relation = db.relationship(
        'Country', backref='espe_etudiee', lazy='joined')

    def __repr__(self):
        return 'f<Life_expectancy {self.l_e_country,\
            self.l_e_year, self.l_e_value }>'
    
    def populate():
        colonnes_l_e = ["l_e_country", "l_e_year", "l_e_value"]
        life_exp = get_life_expectancy()
        lifeX_frame = life_exp
        life_exp.columns = colonnes_l_e
        life_exp = life_exp.to_sql(
                'life_expectancy',
                con=db.engine,
                if_exists="append",
                index=False)
        print("Life_expectancy populated")
        return "done"

    def delete():
        Life_expectancy.__table__.drop(engine)
        print("Life_expectancy deleted")
        return 'done'

class Unemployment_rate(db.Model):
    id_unemp_rate = db.Column(db.Integer, primary_key=True)
    u_r_country = db.Column(db.String(120))
    u_r_year = db.Column(db.Integer)
    u_r_value = db.Column(db.Float)
    u_r_relation = db.relationship(
        'Country', backref='chom_etudie', lazy='joined')
    
    def __repr__(self):
        return 'f<Unemployment_rate {self.u_r_country,\
            self.u_r_year, self.u_r_value }>'
    
    def populate():
        colonnes_u_r = ['u_r_country','u_r_year','u_r_value']
        taux_chomage = get_unemployment_rate()
        chom_frame = taux_chomage
        taux_chomage.columns = colonnes_u_r
        taux_chomage = taux_chomage.to_sql(
                'unemployment_rate',
                con=db.engine,
                if_exists="append",
                index=False)
        print("Unemployment_rate populated")
        return "done"

    def delete():
        Unemployment_rate.__table__.drop(engine)
        print("Unemployment_rate deleted")
        return 'done'

    
class Country(db.Model):
    id_country = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(120), index=True)
    country_pop = db.Column(db.Integer, db.ForeignKey(
        'population.id_population'))
    country_life_exp = db.Column(db.Integer, db.ForeignKey(
        'life_expectancy.id_life_expe'))
    country_unem_rate = db.Column(db.Integer, db.ForeignKey(
        'unemployment_rate.id_unemp_rate'))
    country_temp = db.Column(db.Integer, db.ForeignKey(
        'temperature.id_temperature'))
    country_temp_5d = db.Column(db.Integer, db.ForeignKey(
        'temperature_5days.id_temp_5days'))
    country_weather_5d = db.Column(db.Integer, db.ForeignKey(
        'weather_5days.id_weather_5days'))
    
    def __repr__(self):
        return 'f<Country {self.country_name}>' 


    def populate():
        countries = get_countries_populated()
        countries = countries.to_sql(
            'country',
            con=db.engine,
            if_exists='append',
            index=False)
        print("Country populated")
        return "done"

    def delete():
        Country.__table__.drop(engine)
        print("Country deleted")
        return 'done'


def populate_all_tables():
    Population.populate()
    Unemployment_rate.populate()
    Life_expectancy.populate()
    Temperature.populate()
    Weather_5days.populate()
    Temperature_5days.populate()
    Country.populate()
    
    print("All tables populated")
    return "done"

def delete_all_tables():
    """
    To do : Save in an another database deleted data
    """
    Population.delete()
    Unemployment_rate.delete()
    Life_expectancy.delete()
    Temperature.delete()
    Weather_5days.delete()
    Temperature_5days.delete()
    Country.delete()
    
    print("All tables deleted")
    return "done"
