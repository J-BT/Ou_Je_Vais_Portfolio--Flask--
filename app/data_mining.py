import pandas as pd
import numpy as np
import json
import pprint
from countryinfo import CountryInfo
import time, datetime, os
import requests
try:
    from app import engine
except:
    print(""" 'engine' not importable from this file """)


def countries_names_trigrams():
    '''
    We import countries names & trigrams from the excel file in static directory.
    To access to the country list : name_dict["countries_names"]  
    To access to the trigrams list : name_dict["countries_trigrams"]
    '''
    names_trigrams = {}
    pays = pd.read_excel('app/static/excel/oecd_country_code.xls')
    nom_des_pays = pays['Country']
    nom_des_pays = nom_des_pays.values.tolist()
    code_pays = pays['CODE']
    code_pays = code_pays.values.tolist()
    code_pays_oecd = '+'.join(code_pays)
    names_trigrams["countries_names"] = nom_des_pays
    names_trigrams["countries_trigrams"] = code_pays_oecd

    return names_trigrams 

def get_from_oecd(sdmx_query):
    """
    Enable to import OECD informations through its API.
    In this module we are going to replace {sdmx_query} variable with 
    'DataSetCode' (as HEALTH_STAT, HISTPOP,..?), 
    'Subject' (EVIETOTA.EVIDUREV+EVIFHOEV+EVIHFEEV),
    etc.
    ==> No key is needed !!!
    """
    return pd.read_csv(
    f"https://stats.oecd.org/SDMX-JSON/data/{sdmx_query}all?"
    +"&dimensionAtObservation=allDimensions&contentType=csv"
    )

def get_population():
    '''
    We retrieve the number of inhabitants in the countries list stored
    in the variable {code_pays_oecd} from 2000.
    '''
    demograph = f"HISTPOP/{code_pays_oecd}.T.TOTAL/all"
    get_from_oecd(demograph)    
    total_habitants = get_from_oecd(demograph)    
    masque = (total_habitants["Time"] >= 2000)    
    population = total_habitants[masque]
    population = population.sort_values(by=['Country','Time'], ascending=True)
    population = population[['Country','Time','Value']]
    population['Country'] = population['Country'].apply(lambda x: x.upper())
    population['Value'] = population['Value'].apply(
        lambda x: int(x))
    
    #Let's reindex the dataframe
    new_index = [] 
    for index in range(1, len(population.index)+1):
        new_index.append(index)
    population.index = new_index
    
    return population

def get_unemployment_rate():
    '''
    We retrieve the ratio of unemployed persons in the countries list
    stored in the variable {code_pays_oecd} from 2000.
    '''

    tx_chom = f"LFS_SEXAGE_I_R/{code_pays_oecd}.MW.900000.UR.A/"
    get_from_oecd(tx_chom)    
    chomage = get_from_oecd(tx_chom)    
    masque = (chomage["Time"] >= 2000 )
    taux_chomage = chomage[masque]
    taux_chomage = taux_chomage.sort_values(by=['Country','Time'],
                                                              ascending=True)
    taux_chomage = taux_chomage[['Country','Time','Value']]
    taux_chomage['Country'] = taux_chomage['Country'].apply(
        lambda x: x.upper())
    taux_chomage['Value'] = taux_chomage['Value'].apply(
        lambda x: round(x, 2))
    #Let's reindex the dataframe
    new_index = [] 
    for index in range(1, len(taux_chomage.index)+1):
        new_index.append(index)
    taux_chomage.index = new_index
    
    return taux_chomage

def get_life_expectancy():
    '''
    We retrieve the life_expectancy ratio in the countries list
    stored in the variable {code_pays_oecd} from 2000.
    '''

    espe_vie = "HEALTH_STAT/EVIETOTA.EVIDUREV+EVIFHOEV+EVIHFEEV."
    espe_vie+= f"{code_pays_oecd}/"
    get_from_oecd(espe_vie)
    espe = get_from_oecd(espe_vie)
    # Importation of data > 2000
    masque = (espe.Year >= 2000)
    espe_2000_2018 = espe[masque]
    # Life expectancy table ranking
    espe_2000_2018 = espe_2000_2018.sort_values(by=['Country','Year'],
                                                ascending=True)
    espe_2000_2018 = espe_2000_2018[['Country','Year','Value']]
    espe_2000_2018['Country'] = espe_2000_2018['Country'].apply(
        lambda x: x.upper())
    espe_2000_2018['Value'] = espe_2000_2018['Value'].apply(
        lambda x: round(x, 2))
    #Let's reindex the dataframe
    new_index = [] 
    for index in range(1, len(espe_2000_2018.index)+1):
        new_index.append(index)
    espe_2000_2018.index = new_index
    
    return espe_2000_2018

def get_timestamp_for_5_days():
    """
    Create a dictionnary {day : timestamp}. This means the following
    values stand for the last 5 days at the same hour.
    
    ***********************************************************
    *****    The timestanp format is in  milliseconds     *****
    ***********************************************************
    ___________________________________________________________________
    >>>>>> 432000 = 5*24h | 86400 =  24h | 3600 = 1h <<<<<<<<<<<<<<<<<<
    ------------------------------------------------------------------
    {
    day-5 : x + 86400*0
    day-4 : x + 86400*1
    day-3 : x + 86400*2
    day-2 : x + 86400*3
    day-1 : x + 86400*4
    }
    where x = actual time - 432000
    
    --- for example ---
    if actual time = Timestamp('2020-11-12 13:52:19.670039') = 1605189139
    x = 1605189139 - 5 days = 1605189139 - 432000 = 1604757139
        L> where 1604757139 equal 11/07/2020 @ 1:52pm (UTC)
    
    day-5 : x + 86400*0 = 1604757139  # 07/11/2020 @ 13:52 (UTC)
    day-4 : x + 86400*1 = 1604843539  # 08/11/2020 @ 13:52 (UTC)
    day-3 : x + 86400*2 = 1604929939  # 09/11/2020 @ 13:52 (UTC)
    day-2 : x + 86400*3 = 1605016339  # 10/11_2020 @ 13:52 (UTC)
    day-1 : x + 86400*4 = 1605102739  # 11/11/2020 @ 13:52 (UTC)

    
    """
    
    datestamps_5_jours = {}
    
    datetime_now_for_humans = pd.Timestamp.now()
    # L> for instance x: Timestamp('2020-11-12 13:27:58.668275')
    
    # We convert in timestamp format
    datetime_now_for_machines = pd.Timestamp.timestamp(
        datetime_now_for_humans)
    datetime_now_for_machines = int(datetime_now_for_machines)
    # L> for example : 1605187678.668275
    m_5days = datetime_now_for_machines - 432000
    
    for i in range(5, 0, -1):
        datestamps_5_jours[f"day_m{i}"] = m_5days + 86400*(5-i)
        
        
    return datestamps_5_jours

def capitales_etudiee_oecd():
    '''
    Enable to retrieve OECD countries capitals through CountryInfo() method.
    This is useful for OpenWeatherMap informations extracting.

    ==> Countries capitals are return in a dictionnary as follows:
    {
    ...
    'SRI LANKA': 'Colombo',
    'SUDAN': 'Khartoum', etc
    ...
    }

    '''
    with open('app/static/json/city.list.json') as f:
        data = json.load(f)
    capitales_oecd = {}
    nom_pays_ocde_majuscules = []
    nom_pays_open_weather_majuscules = []
    pays_communs_pour_projet = []
    
    for pays in nom_des_pays:
        nom_pays_ocde_majuscules.append(pays.upper())    
    infos_pays = CountryInfo()
    infos_pays = infos_pays.all()
    infos_pays = dict(infos_pays)
    
    for pays in infos_pays.keys():
        nom_pays_open_weather_majuscules.append(pays.upper())
    
    ### Creation of a set in order to find similar cities within lists
    pays_ocde = set(nom_pays_ocde_majuscules)
    pays_open_weather = set(nom_pays_open_weather_majuscules)
    pays_communs_pour_projet = pays_ocde.intersection(pays_open_weather)
    
    ### Converting set in list
    pays_communs_pour_projet = list(pays_communs_pour_projet)
    pays_communs_pour_projet.sort(reverse=False)
    
    for pays in pays_communs_pour_projet:
        country = CountryInfo(pays)
        # capitale = country.capital().upper()
        capitale = country.capital()
        capitales_oecd[pays] = capitale    
        
    return capitales_oecd

def get_latitute_and_longitude():
    """
    Imports capitals and shows their latitute and longitude
    
    ---format----
    { COUNTRY : ["Capital", [latitude, longitude]] }
    
    """
    lat_long_capitales ={}
    for pays, capitale in capitals.items():
        lat_long = CountryInfo(pays)
        try:
            lat_long = lat_long.capital_latlng()
        except:
            lat_long = "erreur"
        lat_long_capitales[pays] = [capitale, lat_long]
        
    return lat_long_capitales

def get_temperature():
    """
    Collection of actual temperatures in the captitals of countries belonging
    to the OECD
    """
    capitales_monde = []
    def temperatures_du_monde(villes):
        """
        Gets some informations from OpenWeatherMap API about actual temperatures
        within OECD countries.
        The function return a list of dictionnary as following.
        <---- Format ----> 
        [{country1} : {temperature1},
         {country2} : {temperature2},
         ...]
        """
        def temperature_actuelle_pays(ville):
            API_key_1 = os.environ.get('CLE_OPENWEATHER_1')
            url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}"
            url+= f"&appid={API_key_1}"
            reponse = requests.get(url)
            
            resultat = reponse.json()
            infos_pays = {}
            try:
                # country name
                pays = resultat['sys']['country']
            except:
                pays = "erreur"
                # print(pays)
            try:
                # ville 
                la_ville = ville
            except:
                ville = 'erreur'
            try:
                # actual temperatures in Kelvin
                temperature_kelvin = resultat['main']['temp']
            except:
                temperature_kelvin = 'erreur'
            
            try:
                # actual temperatures in °C
                temperature_c = round((temperature_kelvin - 273.15), 2)
            except:
                temperature_c = 'erreur'
            infos_pays[pays]= [ville, temperature_kelvin, temperature_c]
            # print(infos_pays)
            return infos_pays
        
        temperatures_villes = {}
        for ville in villes:
            for cle, valeur in temperature_actuelle_pays(ville).items():
                temperatures_villes[cle] = valeur
                # print(temperatures_villes[rang_ville])
        return temperatures_villes
    
    capitales = capitales_etudiee_oecd()
    capitales_oecd = list(capitales.values())
    # print(capitales_oecd)
    
    temperature_pays = temperatures_du_monde(capitales_oecd)
   
    # print(temperature_pays)
    # print(type(temperature_pays))
    
    ### Creation dictionnaire pour df puis table climat
    temperatures_pays_bdd = {}
    
    for code, capitale_kelvin_celcius in temperature_pays.items():
        # print(capitale_kelvin_celcius)
        for pays, capitale in capitales.items():
            if capitale_kelvin_celcius[0] == capitale:
                date_temp = []
                date_temp.append(pd.Timestamp.today())
                date_temp.append(capitale_kelvin_celcius[2])
                temperatures_pays_bdd[pays] = date_temp
    
    temperature_pays = temperatures_pays_bdd
    temp_part1 = pd.DataFrame(temperature_pays.keys())
    todays = []
    temperatures = []
    for today, temperature in temperature_pays.values():
        todays.append(today)
        temperatures.append(temperature)  
    temp_part1[1] = pd.DataFrame(todays)
    temp_part1[2] = pd.DataFrame(temperatures)
    temp_columns = ['temp_country','temp_today','temp_value']
    temp_part1.columns = temp_columns
    countries_temperature = temp_part1
    
### errors' suppression inside temperature dataframe
    masque = (countries_temperature['temp_country'] != 'erreur') &\
        (countries_temperature['temp_today'] != 'erreur') &\
        (countries_temperature['temp_value'] != 'erreur')
    countries_temperature = countries_temperature[masque]
    # print("Appel fonction réussi!")
    return countries_temperature

def get_historical_5_previous_days():
    """
    In order to retrieve the 5 last days weather statements (day by day,
    hour by hour) and to store them inside the 2 following panda's dataframes:
        - Five_days_previous_temperatures  (historique temperatures)
        - Five_days_previous_weather (historique méteo)
    
    This function: 
        
    1) Imports latitudes and longitudes of OECD ,capitals cities
    
    2) Uses pandas.Timestamp.now() to convert actual time in Timestamp format

    3) Creates 5 variables corresponding respectively to the actual time -5 days,
    -4 days, ..., -1 days 
     
    4) Gets weather informations thanks to the API entry point :
         ______________________________________________________________
    ____|| API Instruction for use for 5 last days historical weather ||________

        'http://api.openweathermap.org/data/2.5/onecall/timemachine?'+
        'lat={lat}&lon={long}&dt={timestamp}&appid={API key}'
    ==================================================================== 
    Retrieved infos :
        
        - date (hourly) j / h (TimeStamp) --> [hourly][dt]
        - temperature (hourly) j / h  ---> [hourly][temp]
        
        - weather condition (id) j / h ----------> [hourly][weather][id]
            (clear : 800)
            (11-25% cloudy : 801)
            (25-50% cloudy : 802)
        
        - weather condition (word) j  / h ----------> [hourly][weather][main]
            ("rain", "snow", "clear")
        - weather condition (details) / h 
                -----> [hourly][weather][description]
    =======================================================================
    """
    # Retrieving countries' latitude and longitude
    lat_long_capitales = get_latitute_and_longitude()
    # retieving of hte last 5 days timestamps
    datestamp_5j = get_timestamp_for_5_days()
    
    # dico_test = {}
    # creation of a dictionnary to set an in dex to the dataframe

    ligne = 1
    longitude, latitude, timestamp = 0, 0, 0
    infos_meteo_24h = {}
    infos_temperature_24h = {}
    
    temps_debut_fx = pd.Timestamp.now()
    
    for pays, cap_lat_lon in lat_long_capitales.items():
        for jour, t_stamp in datestamp_5j.items():
            # print(cap_lat_lon)
            latitude = cap_lat_lon[1][0]
            longitude = cap_lat_lon[1][1]
            timestamp = t_stamp
            # dico_test[index] = [pays, latitude, longitude, timestamp]        
            # index += 1
            # print(index, latitude, longitude, pd.to_datetime(timestamp, unit='s'))
            
            API_key_2 = os.environ.get('CLE_OPENWEATHER_2')
            url  = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
            url += f"?lat={latitude}&lon={longitude}&dt={timestamp}&units=metric"
            url += f"&appid={API_key_2}"
            try:
                reponse = requests.get(url)
                resultat = reponse.json()
                pays = pays
                ville = cap_lat_lon[0]
                
                for i in range(len(resultat["hourly"])):
                    #format conversion datetime ms--->datetime

                    datetime_ts = resultat["hourly"][i]["dt"]
                    #format conversiont datetime ms--->datetime
                    datetime = pd.to_datetime(datetime_ts, unit='s')
                    temperature = resultat["hourly"][i]["temp"]
                    weather_id = resultat["hourly"][i]["weather"][0]["id"]
                    weather_main = resultat["hourly"][i]["weather"][0]["main"]
                    weather_description = resultat["hourly"][i]["weather"][0]["description"]
                
                    infos_temperature_24h[ligne] = [pays, ville,
                                                    datetime, temperature]
                    infos_meteo_24h[ligne] = [pays, ville, datetime,
                                              weather_id, weather_main,
                                              weather_description]
                    
                    ligne += 1
            except:
                datetime = pd.to_datetime(timestamp, unit='s')
                infos_temperature_24h[ligne] = [pays, ville, datetime, 'NaN']
                infos_meteo_24h[ligne] = [pays, ville, datetime,'NaN',
                                          'NaN', 'NaN']
                ligne += 1
    
    # Creation of DF with historical temperatures
    historical_temperatures_5days = pd.DataFrame(
        infos_temperature_24h.values())
    colonnes = ["temp_5days_country","temp_5days_city",
                "temp_5days_date", "temp_5days_value" ]
    historical_temperatures_5days.columns = colonnes
    historical_temperatures_5days.sort_values(by=['temp_5days_country',
                                                  'temp_5days_date'],
                                              ascending=True)
    
    # Creation of DF with historical weather
    historical_weather_5days = pd.DataFrame(infos_meteo_24h.values())
    colonnes = ["weather_5days_country","weather_5days_city",
                "weather_5days_date", "weather_5days_w_id",
                "weather_5days_w_main", "weather_5days_w_descrip" ]
    historical_weather_5days.columns = colonnes
    historical_weather_5days.sort_values(by=['weather_5days_country',
                                             'weather_5days_date'],
                                         ascending=True)
    
    
    # removing of 'NaN' values
    sans_NaN = (historical_temperatures_5days['temp_5days_date'] != 'NaN') &\
            (historical_temperatures_5days['temp_5days_value'] != 'NaN') 
    historical_temperatures_5days = historical_temperatures_5days[sans_NaN]
    
    # removing of 'NaN' values
    sans_NaN = (historical_weather_5days['weather_5days_date'] != 'NaN') &\
            (historical_weather_5days['weather_5days_w_id'] != 'NaN') &\
            (historical_weather_5days['weather_5days_w_main'] != 'NaN')&\
            (historical_weather_5days['weather_5days_w_descrip'] != 'NaN')
    historical_weather_5days = historical_weather_5days[sans_NaN]
    
    temps_fin_fx = pd.Timestamp.now()
           
    
    temps_execution_fonction =  temps_fin_fx - temps_debut_fx
    print("temps execution f(x) = ", temps_execution_fonction)
    
    return historical_temperatures_5days, historical_weather_5days    

def get_countries_populated():
    """
    A pour but de peupler la df Country avec les index des differentes
    tables (Life_exceptancy, Pupulation...) qui permettront de d'indiquer les
    foreign key de la table Country
    
    """
    pays_analyses = pd.DataFrame(nom_des_pays, columns =['country_name'])
    pays_analyses['country_name'] = pays_analyses['country_name'].apply(
        lambda x: x.upper())
    pays_analyses = pays_analyses.sort_values(by=['country_name'],
                                              ascending=True)
  
    # adding new columns
    pays_analyses['country_pop'] = None
    pays_analyses['country_life_exp'] = None
    pays_analyses['country_unem_rate'] = None
    pays_analyses['country_temp'] = None
    pays_analyses['country_temp_5d'] = None
    pays_analyses['country_weather_5d'] = None
    
    espe_2000_2018 = pd.read_sql_table("life_expectancy", engine)
    population = pd.read_sql_table("population", engine)
    taux_chomage = pd.read_sql_table("unemployment_rate", engine)
    temp_actuelle = pd.read_sql_table("temperature", engine)
    temp_5j_av = pd.read_sql_table("temperature_5days", engine)
    meteo_5j_av = pd.read_sql_table("weather_5days", engine)
           
    mask_2017 = espe_2000_2018["l_e_year"] == 2017
    espe_2017 = espe_2000_2018[mask_2017]
    
    mask_2017 = population["pop_year"] == 2017
    pop_2017 = population[mask_2017]
    
    mask_2017 = taux_chomage["u_r_year"] == 2017
    chom_2017 = taux_chomage[mask_2017]
    
    ###---------------------------------------------------------------
    # country_temp_5d & country_weather_5d column
    #-----------------------------------------------------------------
    ts_moins_5j =  temp_5j_av['temp_5days_date'][12]

    mask_midi = temp_5j_av['temp_5days_date'] == ts_moins_5j
    temp_5days_av_midi = temp_5j_av[mask_midi]
    
    mask_midi = meteo_5j_av['weather_5days_date'] == ts_moins_5j
    meteo_5days_av_midi = meteo_5j_av[mask_midi]
    
    

    # Condition = only select countries within OECD 
    condition = pays_analyses['country_name'].isin(
        espe_2000_2018['l_e_country'])
    
 
    ### Let's populate df Country -> population
    for index_pays, ligne_pays in pays_analyses.iterrows():
        # print(f'Index: {index}, ligne_pays: {ligne_pays.values[0]}')
        # ligne_pays.values[1]= 33
        for index_pop, ligne_pop in pop_2017.iterrows():
            # print(f'Index: {index}, ligne_pays: {ligne_espe.values}')
            if ligne_pays[0] == ligne_pop[1]:
                ligne_pays[1] = ligne_pop[0]
    ### Let's populate df Country -> life expectancy
        for index_espe_vie, ligne_espe in espe_2017.iterrows():
            # print(f'Index: {index_espe_vie}, ligne_pays: {ligne_espe.values}')
            if ligne_pays[0] == ligne_espe[1]:
                ligne_pays[2] = ligne_espe[0]
                
    ### Let's populate df Country -> unemployment_rate
        for index_chom, ligne_chom in chom_2017.iterrows():
            # print(f'Index: {index}, ligne_pays: {ligne_espe.values}')
            if ligne_pays[0] == ligne_chom[1]:
                ligne_pays[3] = ligne_chom[0]
    
    ### Let's populate -> actual temperature
        for index_temp, ligne_temp in temp_actuelle.iterrows():
            if ligne_pays[0] == ligne_temp[1]:
                ligne_pays[4] = ligne_temp[0]
     
    ### Let's populate-> 5 last days temperatures 
        for index_temp5j, ligne_temp5j in temp_5days_av_midi.iterrows():
            if ligne_pays[0] == ligne_temp5j[1]:
                ligne_pays[5] = ligne_temp5j[0]
    
    ### Let's populate-> 5 last days weather conditions
        for index_meteo5j, ligne_meteo5j in meteo_5days_av_midi.iterrows():
            if ligne_pays[0] == ligne_meteo5j[1]:
                ligne_pays[6] = ligne_meteo5j[0]

    return pays_analyses

names_and_trigrams_lists = countries_names_trigrams()
code_pays_oecd = names_and_trigrams_lists["countries_trigrams"]
nom_des_pays = names_and_trigrams_lists["countries_names"]
capitals = capitales_etudiee_oecd()

if __name__ == "__main__":
    ## -- To load the env variables from this file
    from dotenv import load_dotenv
    basedir = os.path.realpath(".env")
    load_dotenv(basedir)
    ## --------------------------------------------
    # temp_histo = get_historical_5_previous_days()
    # print(temp_histo)
    print("ça marche ")
