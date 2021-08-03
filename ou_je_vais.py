import pandas as pd
from app import create_app, db
from app.models import (User, Message_user, Weather_5days,
 Temperature_5days, Temperature, Population, Life_expectancy,
 Unemployment_rate, Country)

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Message_user': Message_user,
        'Weather_5days' : Weather_5days,
        'Temperature_5days' : Temperature_5days,
        'Temperature' : Temperature,
        'Population' : Population,
        'Life_expectancy' : Life_expectancy,
        'Unemployment_rate' : Unemployment_rate,
        'Country' : Country
        }

        