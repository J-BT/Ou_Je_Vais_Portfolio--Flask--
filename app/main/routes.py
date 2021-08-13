from app import (db, engine, session)
from flask import (render_template, redirect, url_for, flash, request, json)
from flask_login import (current_user, login_user, logout_user, login_required)
from werkzeug.urls import url_parse
import pandas as pd
import json
from app.main import bp
from app.main.forms import (Choix_utilisateur)
from app.models import (Life_expectancy,
                        Country,
                        Unemployment_rate,
                        Population,
                        Temperature, 
                        Weather_5days,
                        Temperature_5days,
                        Message_user,
                        User)

from app.data_visualization import (lineplot_analyse, graph_corr)


@bp.route('/')
@bp.route("/Accueil", methods= ['GET','POST'] )
def accueil():
    technologiesUtilisees = {
        "frontend" : ["HTML", "CSS", "Javascript", "Boostrap"],
        "backend" : ["Python", "Flask", "Pandas", "Matplotlib"],
        "bdd" : ["PostgreSQL", "SQLAlchemy", "PgAdmin"],
        "serveur" : ["Digital Ocean", "Ubuntu Server", "NGINX", "Git / GitHub"]
    }

    return render_template('index.html', title="Page d'Accueil",
     technologiesUtilisees=technologiesUtilisees)


@bp.route("/Contact", methods= ['GET','POST'] )
def contact():
    if request.method == "POST":
        nom_contact = request.form['contact_name']
        email_contact = request.form['contact_email']
        msg_contact = request.form['contact_message']


        # Sauvegarde du message envoyé par le contact
        # dans la table Message_user
        message_utilisateur = Message_user(
            username = nom_contact,
            email = email_contact,
            contenu = msg_contact)

        db.session.add(message_utilisateur)
        db.session.commit()


        est_ce_que_user = bool(User.query.filter_by(
                username=nom_contact))
        # Mise à jour de table User
        # Si l'utilisateur existe dans bdd
        if est_ce_que_user:
            msg = pd.read_sql_table("message_user", engine)
            #id du dernier msg envoyé par l'utilisateur
            id_nouveau_msg = msg[
                msg["username"]==nom_contact].tail(1)["id_msg_u"]
            id_nouveau_msg = int(id_nouveau_msg) # on convert en int

            ajout_id_msg_ds_User = session.query(
                User
            ).filter(
                User.username==nom_contact
            ).update(
                {User.msg_user : id_nouveau_msg}
            )
            session.commit()
          
        
        flash(f'Message envoyé !', 'success')
        flash(f'Merci M.Mme {nom_contact} !', 'success')
        
        return render_template(
            'index.html')
    
    elif request.method == 'GET':
        technologiesUtilisees = {
            "frontend" : ["HTML", "CSS", "Javascript", "Boostrap"],
            "backend" : ["Python", "Flask", "Pandas", "Matplotlib"],
            "bdd" : ["PostgreSQL", "SQLAlchemy", "PgAdmin"],
            "serveur" : ["Digital Ocean", "Ubuntu Server", "NGINX", "Git / GitHub"]
        }
        return render_template(
            'contact.html',
            title = 'Contact', technologiesUtilisees = technologiesUtilisees)


##### API ###################################################################

@bp.route("/Classement_pays/<string:classer_par>/<string:type_de_classement>/", 
    methods= ['GET'] )
def classement_pays(classer_par, type_de_classement):
    """
    Donne acces à la table Pays.
    Dans l'url remplacer par l'un des mots suivants :

    [classer_par] : 
            - id_country
            - country_name
            - country_pop
            - country_life_exp
            - country_unem_rate
            - country_temp
            - country_temp_5d
            - country_weather_5d


    [type_de_classement] :
            - croissant
            - decroissant

    """
    try:

        les_pays = session.query(Country).filter(
            Country.country_pop.isnot(None),
            Country.country_life_exp.isnot(None),
            Country.country_unem_rate.isnot(None),
            Country.country_temp.isnot(None),
            Country.country_temp_5d.isnot(None),
            Country.country_weather_5d.isnot(None),
                                            )
        p_valeurs_pr_classement = {}
        index = 1
        for ce_pays in les_pays:
            p_valeurs_pr_classement[index] = [
                ce_pays.id_country,
                ce_pays.country_name,
                ce_pays.pop_etudie.pop_value,
                ce_pays.espe_etudiee.l_e_value,
                ce_pays.chom_etudie.u_r_value,
                ce_pays.temp_etudie.temp_value,
                ce_pays.temp_5j_etudiee.temp_5days_value,
                ce_pays.weather_5j_etudie.weather_5days_w_main]
            index += 1

        colonnes = [
            "id_country",
            "country_name",
            "country_pop",
            "country_life_exp",
            "country_unem_rate",
            "country_temp",
            "country_temp_5d",
            "country_weather_5d"]   
        countries_for_ranking = pd.DataFrame(p_valeurs_pr_classement).T
        countries_for_ranking.columns = colonnes
    
    except:
        print("Pas encore de valeurs dans Country")

    classement_croissant = ""
    
    #type_de_classement = "decroissant"
    #classer_par = "country_pop"
    
    if type_de_classement == "croissant":
        classement_croissant = True
    elif type_de_classement == "decroissant":
        classement_croissant = False
    else:
        return "Erreur"
    classement = countries_for_ranking.sort_values(
        by=[classer_par],
        ascending=classement_croissant)
    classement = classement.head(10)

    classement_pays = classement.to_json(orient="split")
    classement_pays = json.loads(classement_pays)
    json.dumps(classement_pays, indent=4)

    return (classement_pays)


############  TEST  AJAX ######################################################
@bp.route('/Jy_vais_new', methods=['GET'])
def jy_vais_new():
    return render_template('jy_vais_new.html')

@bp.route('/Jy_vais_DATA', methods=['POST'])
def jy_vais_DATA():
    if request.method == "POST":
        user =  request.form['username']
        password = request.form['password']
        return json.dumps({'status':'OK','user':user,'pass':password},
                        indent=4)


# ex : Pour avoir classement pas temperature croissante
#  Dans l'url taper ----> http://127.0.0.1:5000/Lets_go/country_temp

@bp.route("/Lets_go",
methods= ['POST','GET'] )
def lets_go():
    try:

        les_pays = session.query(Country).filter(
            Country.country_pop.isnot(None),
            Country.country_life_exp.isnot(None),
            Country.country_unem_rate.isnot(None),
            Country.country_temp.isnot(None),
            Country.country_temp_5d.isnot(None),
            Country.country_weather_5d.isnot(None),
                                            )
        p_valeurs_pr_classement = {}
        index = 1
        for ce_pays in les_pays:
            p_valeurs_pr_classement[index] = [
                ce_pays.id_country,
                ce_pays.country_name,
                ce_pays.pop_etudie.pop_value,
                ce_pays.espe_etudiee.l_e_value,
                ce_pays.chom_etudie.u_r_value,
                ce_pays.temp_etudie.temp_value,
                ce_pays.temp_5j_etudiee.temp_5days_value,
                ce_pays.weather_5j_etudie.weather_5days_w_main]
            index += 1

        colonnes = [
            "id_country",
            "country_name",
            "country_pop",
            "country_life_exp",
            "country_unem_rate",
            "country_temp",
            "country_temp_5d",
            "country_weather_5d"]   
        countries_for_ranking = pd.DataFrame(p_valeurs_pr_classement).T
        countries_for_ranking.columns = colonnes
    
    except:
        print("Pas encore de valeurs dans Country")

    classement_croissant = ""
    
    type_de_classement = "decroissant"
    classer_par = "country_pop"
    
    if type_de_classement == "croissant":
        classement_croissant = True
    elif type_de_classement == "decroissant":
        classement_croissant = False
    else:
        return "Erreur"
    selon_pop_plus = countries_for_ranking.sort_values(
        by=[classer_par],
        ascending=classement_croissant)
    selon_pop_plus = selon_pop_plus.head(10)

    popMoinsJson = selon_pop_plus.to_json(orient="split")
    popMoinsJson = json.loads(popMoinsJson)
    json.dumps(popMoinsJson, indent=4)

    return (popMoinsJson)

@bp.route("/Jy_vais_AJAX", methods= ['GET'] )
def jy_vais_AJAX():
    
    if request.method == 'GET' :
        technologiesUtilisees = {
            "frontend" : ["HTML", "CSS", "Javascript", "Boostrap"],
            "backend" : ["Python", "Flask", "Pandas", "Matplotlib"],
            "bdd" : ["PostgreSQL", "SQLAlchemy", "PgAdmin"],
            "serveur" : ["Digital Ocean", "Ubuntu Server", "NGINX", "Git / GitHub"]
        }
        try:
            return render_template('lets_go.html',
                                    title = "J'y vais",
                                    technologiesUtilisees=technologiesUtilisees)
        except:
            p = {"France, UK, Japan"}
            return render_template('lets_go.html',
                                    title = "J'y vais",
                                    pays=p,
                                    technologiesUtilisees=technologiesUtilisees)


########### fin TEST AJAX #####################################################

@bp.route("/Jy_vais", methods= ['GET','POST'] )
def jy_vais():
    """
    En se basant sur les bases de données de l'OCDE et celle
    du service en ligne de prévisions météorologiques, OpenWeatherMap,
    cette application vous dresse un classement, en fonction des critères
    que vous choisissez, des pays où vous devriez aller pour être
    satisfait.e.s...

    Ce projet etant un prototype, il vous propose de choisir vos préferences selon
    5 critères :

    Le nombre d'habitants : Elevé ou Faible
    L'esperance de vie : Elevée ou Faible
    Le taux de chômage : Elevé ou Faible
    La temperature : Elevée ou Faible
    La météo : Temps clair ou Pluie
    Pour l'instant vous ne pourrez pas selectionner plus d'un critère à la fois.
    Il faudra laisser les autres selecteurs sur "Ignorer" lorsque vous
    selectionnerez un critère.

    Pour cela, cliquez sur l'onglet "J'y vais!", choisissez vos préferences et
    cliquez sur soumettre.

    L'application vous affichera alors les 10 premiers pays, classés selon
    votre choix.
    """

### Création countries_for_ranking
# On crée DF Country sans valeurs nulles : countries_for_ranking
# Afin de lire la table country avec valeur foreign keys
### Si Country sans valeurs -----> pas pris en compte
    try:

        les_pays = session.query(Country).filter(
            Country.country_pop.isnot(None),
            Country.country_life_exp.isnot(None),
            Country.country_unem_rate.isnot(None),
            Country.country_temp.isnot(None),
            Country.country_temp_5d.isnot(None),
            Country.country_weather_5d.isnot(None),
                                            )
        p_valeurs_pr_classement = {}
        index = 1
        for ce_pays in les_pays:
            p_valeurs_pr_classement[index] = [
                ce_pays.id_country,
                ce_pays.country_name,
                ce_pays.pop_etudie.pop_value,
                ce_pays.espe_etudiee.l_e_value,
                ce_pays.chom_etudie.u_r_value,
                ce_pays.temp_etudie.temp_value,
                ce_pays.temp_5j_etudiee.temp_5days_value,
                ce_pays.weather_5j_etudie.weather_5days_w_main]
            index += 1

        colonnes = [
            "id_country",
            "country_name",
            "country_pop",
            "country_life_exp",
            "country_unem_rate",
            "country_temp",
            "country_temp_5d",
            "country_weather_5d"]   
        countries_for_ranking = pd.DataFrame(p_valeurs_pr_classement).T
        countries_for_ranking.columns = colonnes
    
    except:
        print("Pas encore de valeurs dans Country")

        
   
# ### *****On recupere le choix de l'utilisateur
    choix_utilisateur = Choix_utilisateur()
    pop_choix =[
        ('Ignorer','Ignorer'),
        ('Population +','Population +'),
        ('Population -','Population -')
                   ]
    espe_vie_choix =[
        ('Ignorer','Ignorer'),
        ('Esp.de vie +','Esp.de vie +'),
        ('Esp.de vie -','Esp.de vie -')
                   ]
    chom_choix =[
        ('Ignorer','Ignorer'),
        ('Chomage +','Chomage +'),
        ('Chomage -','Chomage -')
                   ]
    tempe_choix =[
        ('Ignorer','Ignorer'),
        ('Temperature +','Temperature +'),
        ('Temperature -','Temperature -')
                   ]
    meteo_choix =[
        ('Ignorer','Ignorer'),
        ('Météo +','Météo +'),
        ('Météo -','Météo -')
                   ]
    
    choix_utilisateur.nombre_population.choices = pop_choix
    choix_utilisateur.esperance_vie.choices = espe_vie_choix
    choix_utilisateur.taux_chomage.choices = chom_choix
    choix_utilisateur.temperature.choices = tempe_choix
    choix_utilisateur.meteo.choices = meteo_choix
    
    
    ##################################################################
    ### Si l'utilisateur valide un choix  (via submit button) ####
    ##################################################################
    if choix_utilisateur.validate_on_submit() and request.method == 'POST' :
        choix_pop = choix_utilisateur.nombre_population.data
        choix_espe = choix_utilisateur.esperance_vie.data
        choix_chomage = choix_utilisateur.taux_chomage.data
        choix_temperature = choix_utilisateur.temperature.data
        choix_meteo = choix_utilisateur.meteo.data
        
### POPULATION ===============================================================      
        if (choix_pop == 'Population +')\
            and(choix_espe == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Ignorer'):
            flash(f'Vous avez choisi une population importante', 'success')
            selon_pop_plus = countries_for_ranking.sort_values(
                by=['country_pop'],
                ascending=False)
            selon_pop_plus = selon_pop_plus.head(10)
            
### 1/10    ###variables pour line chart *********************************
            premier_pays = selon_pop_plus.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_pop_plus.to_dict(orient='records'))
        
       
        elif (choix_pop == 'Population -')\
            and(choix_espe == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Ignorer'):
            flash(f"Vous avez choisi une population peu nombreuse", 'danger')
            
            selon_pop_moins = countries_for_ranking.sort_values(
                by=['country_pop'],ascending=True)
            selon_pop_moins = selon_pop_moins.head(10)

### 2/10    ###variables pour line chart *********************************
            premier_pays = selon_pop_moins.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            

            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_pop_moins.to_dict(orient='records'))

### ESPERANCE DE VIE =========================================================

        if (choix_espe == 'Esp.de vie +')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Ignorer'):
            flash(f'Vous avez choisi une esperance de vie élevée', 'success')
            selon_espe_plus = countries_for_ranking.sort_values(
                by=['country_life_exp'], ascending=False)
            selon_espe_plus = selon_espe_plus.head(10)
            
### 3/10    ###variables pour line chart *********************************
            premier_pays = selon_espe_plus.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)           
            
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_espe_plus.to_dict(orient='records'))
        
        
       
        elif (choix_espe == 'Esp.de vie -')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Ignorer'):
            flash(f'Vous avez choisi une esperance de vie faible', 'danger')
            selon_espe_moins = countries_for_ranking.sort_values(
                by=['country_life_exp'], ascending=True)
            selon_espe_moins = selon_espe_moins.head(10)
            
            
### 4/10    ###variables pour line chart *********************************
            premier_pays = selon_espe_moins.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)            
            
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_espe_moins.to_dict(orient='records'))

### TAUX DE CHOMAGE  =========================================================

        if (choix_espe == 'Ignorer')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Chomage +')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Ignorer'):
            flash(f'Vous avez choisi un taux de chômage élevé', 'danger')
            selon_chom_mauv = countries_for_ranking.sort_values(
                by=['country_unem_rate'], ascending=False)
            selon_chom_mauv = selon_chom_mauv.head(10)
            
            
### 5/10    ###variables pour line chart *********************************
            premier_pays = selon_chom_mauv.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_chom_mauv.to_dict(orient='records'))
        
       
        elif (choix_espe == 'Ignorer')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Chomage -')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Ignorer'):
            flash(f'Vous avez choisi un taux de chômage faible', 'success')
            selon_chom_bon = countries_for_ranking.sort_values(
                by=['country_unem_rate'], ascending=True)
            selon_chom_bon = selon_chom_bon.head(10)
            
            
### 6/10    ###variables pour line chart *********************************
            premier_pays = selon_chom_bon.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_chom_bon.to_dict(orient='records')) 

### TEMPERATURES  =========================================================


        if (choix_espe == 'Ignorer')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Temperature +')\
            and(choix_meteo == 'Ignorer'):
            flash(f'Vous avez choisi une temperature élevée', 'success')
            selon_tempe_plus = countries_for_ranking.sort_values(
                by=['country_temp', 'country_temp_5d'], ascending=False)
            selon_tempe_plus = selon_tempe_plus.head(10)
            
            
            
### 7/10    variables pour line chart *********************************
            premier_pays = selon_tempe_plus.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_tempe_plus.to_dict(orient='records'))
        
       
        elif (choix_espe == 'Ignorer')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Temperature -')\
            and(choix_meteo == 'Ignorer'):
            flash(f'Vous avez choisi une temperature basse', 'danger')
            selon_tempe_moins = countries_for_ranking.sort_values(
                by=['country_temp', 'country_temp_5d'], ascending=True)
            selon_tempe_moins = selon_tempe_moins.head(10)
            
            
### 8/10    ###variables pour line chart *********************************
            premier_pays = selon_tempe_moins.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_tempe_moins.to_dict(orient='records')) 

### METEO  =========================================================


        if (choix_espe == 'Ignorer')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Météo +'):
            flash(f'Vous avez choisi une météo ensoleillée', 'success')
            masque_meteo_plus = (
                countries_for_ranking['country_weather_5d'] == 'Clear')
            selon_meteo_plus = countries_for_ranking[masque_meteo_plus]
            selon_meteo_plus = selon_meteo_plus.sort_values(
                by=['country_temp', 'country_temp_5d'], ascending=False)
            selon_meteo_plus = selon_meteo_plus.head(10)
            
            
### 9/10    ###variables pour line chart *********************************
            premier_pays = selon_meteo_plus.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_meteo_plus.to_dict(orient='records'))
        
       
        elif (choix_espe == 'Ignorer')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Météo -'):
            flash(f'Vous avez choisi une météo peu chaleureuse', 'danger')
            masque_meteo_moins = (
                countries_for_ranking['country_weather_5d'] == 'Rain') |\
            (countries_for_ranking['country_weather_5d'] == 'Clouds')
            selon_meteo_moins = countries_for_ranking[masque_meteo_moins]
            selon_meteo_moins = selon_meteo_moins.sort_values(
                by=['country_temp', 'country_temp_5d'], ascending=True)
            selon_meteo_moins = selon_meteo_moins.head(10)
            
            
### 10/10   ###variables pour line chart *********************************
            premier_pays = selon_meteo_moins.head(1)
            nom_1er_pays = premier_pays["country_name"]
            pays_graph1 = ''
            for le_pays in nom_1er_pays:
                pays_graph1 = le_pays
            
            #Graph population-----------------------------------------------
            population = pd.read_sql_table("population", engine)
            mask = population['pop_country'] == pays_graph1
            population_etudiee = population[mask]
            abscisse = "pop_year"
            ordonnee = "pop_value"
            fichier = "graphiques/population.png"
            lineplot_analyse(population_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Espe vie-----------------------------------------------
            esperance_vie = pd.read_sql_table("life_expectancy", engine)
            mask = esperance_vie['l_e_country'] == pays_graph1
            esperance_vie_etudiee = esperance_vie[mask]
            abscisse = "l_e_year"
            ordonnee = "l_e_value"
            fichier = "graphiques/espe_vie.png"
            lineplot_analyse(esperance_vie_etudiee, abscisse,
                             ordonnee, fichier)
            
            #Graph Chômage-----------------------------------------------
            taux_chomage = pd.read_sql_table("unemployment_rate", engine)
            mask = taux_chomage['u_r_country'] == pays_graph1
            taux_chomage_etudie = taux_chomage[mask]
            taux_chomage_etudie = taux_chomage_etudie.dropna()
            abscisse = "u_r_year"
            ordonnee = "u_r_value"
            fichier = "graphiques/chomage.png"
            lineplot_analyse(taux_chomage_etudie, abscisse,
                             ordonnee, fichier)
            
            #Graph Corrélation Pop/Espe/Chom/Tempe  -----------------------
            tous_les_pays = pd.read_sql_table("country", engine)
            correlation = tous_les_pays[[
                "country_pop", "country_life_exp",
                "country_unem_rate","country_temp"]]
     
            fichier = "graphiques/corelation.png"
            graph_corr(correlation, fichier)
            
            
            return render_template('jy_vais.html',
                                title = pays_graph1,
                                choix_utilisateur=choix_utilisateur,
                                pays=selon_meteo_moins.to_dict(orient='records'))

### AUCUN CRITERE  ===========================================================


        elif (choix_espe == 'Ignorer')\
            and (choix_pop == 'Ignorer')\
            and(choix_chomage == 'Ignorer')\
            and(choix_temperature == 'Ignorer')\
            and(choix_meteo == 'Ignorer'):
            flash(f"Veuillez choisir un critère !", 'danger')
            return redirect(url_for('main.jy_vais'))
     

### AUTRES CAS ==============================================================

        flash(f"Veuillez choisir un seul critère à la fois !", 'danger')
        return redirect(url_for('main.jy_vais'))
    
### Si country vide ----> pas pris en compte! 
    elif request.method == 'GET' :
        technologiesUtilisees = {
            "frontend" : ["HTML", "CSS", "Javascript", "Boostrap"],
            "backend" : ["Python", "Flask", "Pandas", "Matplotlib"],
            "bdd" : ["PostgreSQL", "SQLAlchemy", "PgAdmin"],
            "serveur" : ["Digital Ocean", "Ubuntu Server", "NGINX", "Git / GitHub"]
        }
        try:
            return render_template('jy_vais.html',
                                    title = "J'y vais",
                                    pays=countries_for_ranking.to_dict(
                                        orient='records'),
                                    choix_utilisateur=choix_utilisateur,
                                    technologiesUtilisees=technologiesUtilisees)
        except:
            p = {"France, UK, Japan"}
            return render_template('jy_vais.html',
                                    title = "J'y vais",
                                    pays=p,
                                    choix_utilisateur=choix_utilisateur,
                                    technologiesUtilisees=technologiesUtilisees)
